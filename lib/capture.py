import socket
import struct
import sys
import time

import psutil

# process id to bytes sent mapping
bytes_sent = {}

# process id to bytes received mapping
bytes_received = {}

# process id to established connection time
process_time = {}

def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

def ethernet_head(raw_data):
    dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
    proto = socket.htons(prototype)
    data = raw_data[14:]
    return get_mac_addr(dest), get_mac_addr(src), proto, data

def get_ip(addr):
    return '.'.join(map(str, addr))

def ipv4_head(raw_data):
    version_header_length = raw_data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
    data = raw_data[header_length:]
    return version, header_length, ttl, proto, get_ip(src), get_ip(target), data

def icmp_head(raw_data):
    itype, code, chksum = struct.unpack('! B B H', raw_data[:4])
    return itype, code, chksum, raw_data[4:]

def udp_head(raw_data):
    srcport, destport, length, chksum = struct.unpack('! H H H H', raw_data[:8])
    return srcport, destport, length, chksum, raw_data[8:]

def tcp_head(raw_data):
    pass

def print_protocol(ipv4):
    data = ipv4[6]
    if ipv4[3] == 1:
        icmp = icmp_head(data)
        print('\t - ' + 'ICMP Packet:')
        print('\t\t - ' + 'Type: {}, Code: {}, Checksum: {},'.format(icmp[0], icmp[1], icmp[2]))
        print('\t\t - ' + 'ICMP Data:')
        print('\t\t\t ' + str(icmp[3]))
    elif ipv4[3] == 6:
        tcp = tcp_head(data)
    elif ipv4[3] == 17:
        udp = udp_head(data)
        print('\t - ' + 'UDP Segment:')
        print('\t\t - ' + 'Source Port: {}, Destination Port: {}, Length: {}'.format(udp[0], udp[1], udp[2]))
        print('\t\t - ' + 'UDP Data:')
        print('\t\t\t ' + str(udp[3]))
        get_process(udp[0], udp[1], udp[2])

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

def main():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while True:
        raw_data, addr = s.recvfrom(65535)
        eth = ethernet_head(raw_data)
        print('\nEthernet Frame:')
        print('Interface:', addr[0])
        print('Destination: {}, Source: {}, Protocol: {}'.format(eth[0], eth[1], eth[2]))
        if eth[2] == 8:
            ipv4 = ipv4_head(eth[3])
            print( '\t - ' + 'IPv4 Packet:')
            print('\t\t - ' + 'Version: {}, Header Length: {}, TTL: {},'.format(ipv4[0], ipv4[1], ipv4[2]))
            print('\t\t - ' + 'Protocol: {}, Source: {}, Target: {}'.format(ipv4[3], ipv4[4], ipv4[5]))
            print_protocol(ipv4)

        sys.stdout.flush()

main()