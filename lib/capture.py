import socket
import sys
import os
import time
import psutil

from pparser import parse
from parse.tcp import TCP
from parse.udp import UDP

# refresh intervals to clean up connection and cache
CLEAN_UP = 3

# refresh intervals to re-calculate metrics
UPDATE = 1

# last timestamp before refresh
last_timestamp = time.time()

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

ignoreSame = True

def map_to_process(src_port, dst_port, kind): 
    pid = port_to_process.get(dst_port) if kind == "Incoming" else port_to_process.get(src_port)
    if not pid: 
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if kind == "Incoming":
                if conn.laddr.port == dst_port:
                    port_to_process[dst_port] = conn.pid
                    return conn.pid
            else:
                if conn.laddr.port == src_port:
                    port_to_process[src_port] = conn.pid
                    return conn.pid
    return pid

def track_metric(src_port, dst_port, length, kind):
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
    print("\n+++++++++++++++++++++++++++++++\n")
    print(port_to_process)
    print(bytes_received)
    print(packets_received)
    print(bytes_sent)
    print(packets_sent)
    print("\n+++++++++++++++++++++++++++++++\n")

    """
    current_time = time.time()
    if bytes_sent.get(process_id):
        sent_per_sec = bytes_sent[process_id] / (current_time - process_time[process_id])
        print(f"bytes sent per sec: {sent_per_sec} bytes per second")
    if bytes_received.get(process_id):
        received_per_sec = bytes_received[process_id] / (current_time - process_time[process_id])
        print(f"bytes received per sec: {received_per_sec} bytes per second")
    """

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
            print("No interfaces found.")
            sys.exit(1)
    return interfaces_mac

def main():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    interfaces = get_interfaces_mac()
    while True:
        raw_data, addr = s.recvfrom(65535)
        parsed = parse(raw_data, addr[0], interfaces[addr[0]], ignoreSame)
        if parsed and (isinstance(parsed, TCP) or isinstance(parsed, UDP)):
            data = parsed.getData()
            track_metric(data['src'], data['dst'], data['bytes'], data['type'])
            
        sys.stdout.flush()

main()