import socket
import sys
import os
import time
import psutil
import threading
import math
from datetime import datetime

from lib.pparser import parse
from lib.parse.tcp import TCP
from lib.parse.udp import UDP

ignoreSame = True
capturing = False

# time intervals to clean up connection and cache
CLEAN_UP = 10

# time intervals to re-calculate metrics
UPDATE = 5

# pid to lock mapping for synchronization
process_locks = {}

# last timestamp before refresh
last_timestamp = time.time()

# cached port to process id mapping
port_to_process = {}

# process id to list of ports mapping for cleanup purposes
process_to_ports = {}

# process id to last refresh time mapping
process_refresh_time = {}

# process id to packets sent mapping
packets_sent = {}

# process id to packets received mapping
packets_received = {}

# process id to bytes sent mapping
bytes_sent = {}

# process id to bytes received mapping
bytes_received = {}

def cleanup_pid(pid):
    global process_locks
    global process_refresh_time
    global packets_sent
    global packets_received
    global bytes_sent
    global bytes_received
    global process_to_ports
    global port_to_process
    lock = process_locks.get(pid)
    # check if process has been cleaned
    if not lock:
        return
    with lock:
        print("\n++++++++++++++++++++++++++++++++++++")
        print(f"proces {pid} is dead. Cleaning up...")
        print("++++++++++++++++++++++++++++++++++++\n") 
        sys.stdout.flush()   
        # clean up if it has not been cleaned up yet
        if process_locks.get(pid): 
            del process_locks[pid]
        ports = process_to_ports.get(pid)
        if ports:
            for port in ports:
                if port_to_process.get(port):
                    del port_to_process[port]
        if process_refresh_time.get(pid):
            del process_refresh_time[pid]
        if bytes_received.get(pid):
            del bytes_received[pid]
        if bytes_sent.get(pid):
            del bytes_sent[pid]
        if packets_sent.get(pid):
            del packets_sent[pid]
        if packets_received.get(pid):
            del packets_received[pid]

def cleanup_processes():
    while True:
        time.sleep(CLEAN_UP)
        pids = list(process_locks.keys()) 
        for pid in pids:
            try:
                psutil.Process(pid)
            except:
                # process is dead
                cleanup_pid(pid)

def calc_metric_for_pid(pid):
    global bytes_sent
    global bytes_received
    global packets_sent
    global packets_received
    global process_locks
    global process_refresh_time
    global last_timestamp
    lock = process_locks.get(pid)
    # check if the process has been cleaned
    if not lock:
        return
    with lock:
        # re-check if the process has been cleaned
        if not process_locks.get(pid): 
            return
        # initialize
        bytes_sent_per_s = 0
        bytes_received_per_s = 0
        packets_sent_per_s = 0
        packets_received_per_s = 0
        # get time difference
        current_time = time.time()
        last_refresh_time = process_refresh_time.get(pid)
        if not last_refresh_time:
            last_refresh_time = last_timestamp
        time_diff = current_time - last_refresh_time
        process_refresh_time[pid] = current_time
        # re-calculate metrics
        if bytes_sent.get(pid):
            bytes_sent_per_s = math.ceil(bytes_sent[pid]/time_diff)
            bytes_sent[pid] = 0
        if bytes_received.get(pid):
            bytes_received_per_s = math.ceil(bytes_received[pid]/time_diff)
            bytes_received[pid] = 0
        if packets_sent.get(pid):
            packets_sent_per_s = math.ceil(packets_sent[pid]/time_diff)
            packets_sent[pid] = 0
        if packets_received.get(pid):
            packets_received_per_s = math.ceil(packets_received[pid]/time_diff)
            packets_received[pid] = 0  
        print(f"process {pid}, bytes sent/sec: {bytes_sent_per_s}, bytes received/sec: {bytes_received_per_s}, packets sent/sec: {packets_sent_per_s}, packets received/sec: {packets_received_per_s}") 

def update_metrics():
    global process_locks
    global last_timestamp
    while True:
        # update metrics every UPDATE seconds
        time.sleep(UPDATE)
        print("\n++++++++++++++++++++++++++++++++++++")
        print(f"[{datetime.now()}]")
        # TODO: print system usage
        pids = list(process_locks.keys())
        for pid in pids:
            calc_metric_for_pid(pid)
        print("++++++++++++++++++++++++++++++++++++\n")    
        sys.stdout.flush()
        last_timestamp = time.time()

def validate_connection(port, pid):
    global port_to_process
    global process_to_ports
    if not pid:
        return pid
    pid_ = pid
    try:
        proc = psutil.Process(pid_)
        for conn in proc.connections(kind='inet'):
            if conn.laddr.port == port:
                # validated connection
                return pid_
        # connection ended - update mapping
        if port_to_process.get(port):
            del port_to_process[port]
        if pid_ in process_to_ports:
            if port in process_to_ports[pid_]:
                process_to_ports[pid_].remove(port)
        pid_ = None
    except:
        # process is dead
        cleanup_pid(pid_)
        pid_ = None
    return pid_

def map_to_process(src_port, dst_port, kind):
    global port_to_process
    global process_to_ports
    port = dst_port if kind == "Incoming" else src_port
    pid = port_to_process.get(port)
    pid = validate_connection(port, pid)
    if not pid: 
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.laddr.port == port:
                pid = conn.pid
                port_to_process[port] = pid
                if not process_to_ports.get(pid):
                    process_to_ports[pid] = []
                process_to_ports[pid] += [port]
                break
        if pid and not process_locks.get(pid):
            process_locks[pid] = threading.Lock()
    return pid

def track_metric(src_port, dst_port, length, kind):
    global bytes_received
    global packets_received
    global bytes_sent
    global packets_sent
    global process_locks
    pid = map_to_process(src_port, dst_port, kind)
    if not pid:
        return
    lock = process_locks.get(pid)
    if not lock:
        return
    with lock:
        if kind == "Incoming":
            if not bytes_received.get(pid):
                bytes_received[pid] = 0
            bytes_received[pid] += length
            if not packets_received.get(pid):
                packets_received[pid] = 0
            packets_received[pid] += 1
        else:
            if not bytes_sent.get(pid):
                bytes_sent[pid] = 0
            bytes_sent[pid] += length
            if not packets_sent.get(pid):
                packets_sent[pid] = 0
            packets_sent[pid] += 1

def get_interfaces_mac():
    interfaces_mac = {}
    base_path = "/sys/class/net/"
    for interface in os.listdir(base_path):
        try:
            with open(os.path.join(base_path, interface, 'address'), 'r') as f:
                mac_address = f.read().strip()
            interfaces_mac[interface] = mac_address.upper()
        except IOError:
            print("Interface: {} has been skipped due to missing MAC Address\n".format(interface))
            pass
        if not interfaces_mac:
            print("No interfaces found. Exiting")
            sys.exit(1)
    return interfaces_mac

def get_process_name(pid):
    if not pid:
        return "Unknown (Short-Lived Connections)"
    try:
        process = psutil.Process(pid)
        cmdline = process.cmdline()
        if len(cmdline) > 1:
            return process.name() + " " + cmdline[1] 
        else:
            return process.name()
    except psutil.NoSuchProcess:
        return None

def main():
    threading.Thread(target=update_metrics).start()
    threading.Thread(target=cleanup_processes).start()

    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    interfaces = get_interfaces_mac()
    while True:
        raw_data, addr = s.recvfrom(65535)
        parsed = parse(raw_data, addr[0], interfaces[addr[0]], ignoreSame)
        if parsed and (isinstance(parsed, TCP) or isinstance(parsed, UDP)):
            data = parsed.getData()
            track_metric(data['src'], data['dst'], data['bytes'], data['type'])
        
def begin_capture(writeSniff, writeProc):
    global capturing
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    interfaces = get_interfaces_mac()
    # Start thread here (pass in writeProc to write to process file)
    capturing = True
    while capturing:
        raw_data, addr = s.recvfrom(65535)
        parsed = parse(raw_data, addr[0], interfaces[addr[0]], ignoreSame, writeSniff)
        if parsed and (isinstance(parsed, TCP) or isinstance(parsed, UDP)):
            data = parsed.getData()
            pid = map_to_process(data['src'], data['dst'], data['type'])
            writeSniff('Above Packet is for process: {} (PID: {})\n'.format(get_process_name(pid), pid))
            # Do data stuff here
    s.close()
    return True

def stop_capture():
    global capturing
    capturing = False