from parse.eth import EthFrame
from parse.ipv4 import IPV4
from parse.tcp import TCP
from parse.icmp import ICMP
from parse.udp import UDP

def _print_protocol(ipv4):
    data = ipv4.payload
    protocol = ipv4.proto
    if protocol == 1:
        icmp = ICMP(data)
        print(icmp)
        return
    if protocol == 6:
        tcp = TCP(data, ipv4.kind, ipv4.getPayloadLength())
        print(tcp)
        return
    if protocol == 17:
        udp = UDP(data, ipv4.kind)
        print(udp)
        return

def parse(raw_data, iface, mac_addr, ignoreSame):
    eth = EthFrame(raw_data, iface, mac_addr)
    if ignoreSame and eth.kind == "Loopback":
        return
    print(eth)
    if eth.proto == 8:
        ipv4 = IPV4(eth.payload, eth.kind)
        print(ipv4)
        _print_protocol(ipv4)