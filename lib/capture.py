import socket
import sys
import os
import time
import psutil
import threading
import math

from lib.pparser import parse
from lib.parse.tcp import TCP
from lib.parse.udp import UDP

ignoreSame = True
capturing = False

# refresh intervals to clean up connection and cache
CLEAN_UP = 10

# refresh intervals to re-calculate metrics
UPDATE = 5

# for synchronization
metrics_lock = threading.Lock()

# last timestamp before refresh
last_timestamp = time.time()

# Active processes
processes = {}

# cached port to process id mapping
port_to_process = {}

# process id to packets sent mapping
packets_sent = {}

# process id to packets received mapping
packets_received = {}

# process id to bytes sent mapping
bytes_sent = {}

# process id to bytes received mapping
bytes_received = {}

def update_metrics():
    global bytes_received
    global packets_received
    global bytes_sent
    global packets_sent
    global processes
    global last_timestamp
    global metrics_lock
    while True:
        time.sleep(UPDATE)
        with metrics_lock:
            print("\n++++++++++++++++++++++++++++++++++++")
            current_time = time.time()
            time_diff = current_time - last_timestamp
            last_timestamp = current_time
            for pid in processes:
                bytes_sent_per_s = 0
                bytes_received_per_s = 0
                packets_sent_per_s = 0
                packets_received_per_s = 0
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
            print("++++++++++++++++++++++++++++++++++++\n")                
            sys.stdout.flush()

def map_to_process(src_port, dst_port, kind):
    global port_to_process
    global processes
    pid = port_to_process.get(dst_port) if kind == "Incoming" else port_to_process.get(src_port)
    if not pid: 
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if kind == "Incoming":
                if conn.laddr.port == dst_port:
                    port_to_process[dst_port] = conn.pid
                    pid = conn.pid
                    break
            else:
                if conn.laddr.port == src_port:
                    port_to_process[src_port] = conn.pid
                    pid = conn.pid
                    break
    if not processes.get(pid):
        processes[pid] = True
    return pid

def track_metric(src_port, dst_port, length, kind):
    global bytes_received
    global packets_received
    global bytes_sent
    global packets_sent
    global metrics_lock
    with metrics_lock:
        pid = map_to_process(src_port, dst_port, kind)
        if not pid:
            return
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
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return None

def main():
    threading.Thread(target=update_metrics).start()

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
            writeSniff('Above Packet is for process: {} ({})\n'.format(get_process_name(pid), pid))
            # Do data stuff here
    s.close()
    return True

def stop_capture():
    global capturing
    capturing = False