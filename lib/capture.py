import socket
import sys
import os
from pparser import parse

ignoreSame = True

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

main()