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

# flag to control capturing
capturing = False

# flag for safe exiting
metrics_thread_exited = True

# flag for safe exiting
cleanup_thread_exited = True

# socket timeout
TIMEOUT = 1

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

# system packets sent since last refresh
system_packets_sent = 0

# system packets received since last refresh
system_packets_received = 0

# system bytes sent since last refresh
system_bytes_sent = 0

# system bytes received since last refresh
system_bytes_received = 0

"""
Cleans up datastructures that contain information associated to a dead process pid
"""
def cleanup_pid(pid, writeProc):
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
        writeProc("\n++++++++++++++++++++++++++++++++++++\n")
        writeProc(f"[{datetime.now()}]\n")
        writeProc(f"proces {pid} is dead. Cleaning up...\n")
        writeProc("++++++++++++++++++++++++++++++++++++\n") 
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

"""
Thread function - to clean up any exited process
"""
def cleanup_processes(writeProc):
    global capturing
    global cleanup_thread_exited
    while capturing:
        time.sleep(CLEAN_UP)
        pids = list(process_locks.keys()) 
        for pid in pids:
            try:
                psutil.Process(pid)
            except:
                # process is dead
                cleanup_pid(pid, writeProc)
    cleanup_thread_exited = True


"""
Calculates and print system metrics
"""
def calc_system_metrics(writeProc):
    global system_packets_sent
    global system_packets_received
    global system_bytes_sent
    global system_bytes_received
    global last_timestamp
    cur_bytes_received = 0 
    cur_packets_received = 0
    cur_bytes_sent = 0
    cur_packets_sent = 0
    current_time = time.time()
    time_diff = current_time - last_timestamp
    # parse system metrics from /proc/net/dev
    with open('/proc/net/dev', 'r') as f:
        lines = f.readlines()
    # Skip headers
    metrics = lines[2:]
    for metric in metrics:
        m = metric.split()
        cur_bytes_received += int(m[1])
        cur_packets_received += int(m[2])
        cur_bytes_sent += int(m[9])
        cur_packets_sent += int(m[10])
    bytes_sent_per_s = math.ceil((cur_bytes_sent - system_bytes_sent)/time_diff)
    bytes_received_per_s = math.ceil((cur_bytes_received - system_bytes_received)/time_diff)
    packets_sent_per_s = math.ceil((cur_packets_sent - system_packets_sent)/time_diff)
    packets_received_per_s = math.ceil((cur_packets_received - system_packets_received)/time_diff)
    writeProc(f"System usage, bytes sent/sec: {bytes_sent_per_s}, bytes received/sec: {bytes_received_per_s}, packets sent/sec: {packets_sent_per_s}, packets received/sec: {packets_received_per_s}\n") 
    system_bytes_received = cur_bytes_received
    system_packets_received = cur_packets_received
    system_bytes_sent = cur_bytes_sent
    system_packets_sent = cur_packets_sent

"""
Calculates and print metrics for process pid
"""
def calc_metric_for_pid(pid, writeProc):
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
        writeProc(f"process: {get_process_name(pid)} ({pid}), bytes sent/sec: {bytes_sent_per_s}, bytes received/sec: {bytes_received_per_s}, packets sent/sec: {packets_sent_per_s}, packets received/sec: {packets_received_per_s}\n") 

"""
Thread function - to re-calculate process metrics
"""
def update_metrics(writeProc):
    global process_locks
    global last_timestamp
    global capturing
    global metrics_thread_exited
    while capturing:
        # update metrics every UPDATE seconds
        time.sleep(UPDATE)
        writeProc("\n++++++++++++++++++++++++++++++++++++\n")
        writeProc(f"[{datetime.now()}]\n")
        calc_system_metrics(writeProc)
        pids = list(process_locks.keys())
        for pid in pids:
            calc_metric_for_pid(pid, writeProc)
        writeProc("++++++++++++++++++++++++++++++++++++\n")    
        last_timestamp = time.time()
    metrics_thread_exited = True

"""
Validates that process pid is alive and connected to port. 
If process is dead, it is cleaned up by cleanup_pid()
"""
def validate_connection(port, pid, writeProc):
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
        cleanup_pid(pid_, writeProc)
        pid_ = None
    return pid_

"""
Maps src_port/dst_port to a process, depending on if it is an incoming or outgoing packet.
Returns pid is mapped.
"""
def map_to_process(src_port, dst_port, kind, writeProc):
    global port_to_process
    global process_to_ports
    port = dst_port if kind == "Incoming" else src_port
    pid = port_to_process.get(port)
    pid = validate_connection(port, pid, writeProc)
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

"""
Tracks metrics for process pid.
"""
def track_metric(pid, length, kind):
    global bytes_received
    global packets_received
    global bytes_sent
    global packets_sent
    global process_locks
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

"""
Returns name of process pid
"""
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

"""
Starts packet sniffer and threads that output system metrics
"""
def begin_capture(writeSniff, writeProc):
    global capturing
    global metrics_thread_exited
    global cleanup_thread_exited
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    s.settimeout(TIMEOUT)
    interfaces = get_interfaces_mac()
    capturing = True
    metrics_thread_exited = False
    cleanup_thread_exited = False
    # thread to calculate metrics every UPDATE seconds
    threading.Thread(target=update_metrics, args=(writeProc,)).start()
    # thread to clean up exited processes every CLEAN_UP seconds
    threading.Thread(target=cleanup_processes, args=(writeProc,)).start()
    while capturing:
        try:
            raw_data, addr = s.recvfrom(65535)
            parsed = parse(raw_data, addr[0], interfaces[addr[0]], ignoreSame, writeSniff)
            if parsed and (isinstance(parsed, TCP) or isinstance(parsed, UDP)):
                data = parsed.getData()
                pid = map_to_process(data['src'], data['dst'], data['type'], writeProc)
                writeSniff('Above Packet is for process: {} (PID: {})\n'.format(get_process_name(pid), pid))
                track_metric(pid, data['bytes'], data['type'])
        except socket.timeout:
            continue

    s.close()
    while not (metrics_thread_exited and cleanup_thread_exited):
        time.sleep(0.01)
    return True

"""
Stops sniffer and thread that output system metrics
"""
def stop_capture():
    global capturing
    capturing = False