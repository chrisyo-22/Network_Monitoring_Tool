import socket
import sys
import os
from pparser import parse

import time

import psutil

# process id to bytes sent mapping
bytes_sent = {}

# process id to bytes received mapping
bytes_received = {}

# process id to established connection time
process_time = {}

ignoreSame = True

def get_process(src_port, dst_port, length):
    # if we want to get name:
    # procs = {p.pid: p.info for p in psutil.process_iter(['name'])}
    connections = psutil.net_connections(kind='inet')
    for conn in connections:
        if conn.laddr.port == src_port:
            # sent
            if not process_time.get(conn.pid):
                process_time[conn.pid] = time.time()
            if not bytes_sent.get(conn.pid):
                bytes_sent[conn.pid] = 0
            bytes_sent[conn.pid] += length
            process_id = conn.pid
            break
        elif conn.laddr.port == dst_port:
            # received
            if not process_time.get(conn.pid):
                process_time[conn.pid] = time.time()
            if not bytes_received.get(conn.pid):
                bytes_received[conn.pid] = 0
            bytes_received[conn.pid] += length
            process_id = conn.pid
            break

    current_time = time.time()
    if bytes_sent.get(process_id):
        sent_per_sec = bytes_sent[process_id] / (current_time - process_time[process_id])
        print(f"bytes sent per sec: {sent_per_sec} bytes per second")
    if bytes_received.get(process_id):
        received_per_sec = bytes_received[process_id] / (current_time - process_time[process_id])
        print(f"bytes received per sec: {received_per_sec} bytes per second")

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
        parse(raw_data, addr[0], interfaces[addr[0]], ignoreSame)

        sys.stdout.flush()

main()