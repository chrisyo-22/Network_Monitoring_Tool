from parse.eth import EthFrame
from parse.ipv4 import IPV4
from parse.tcp import TCP
from parse.icmp import ICMP
from parse.udp import UDP
from parse.dns import DNS
    
def parse_ipv4(ipv4):
    data = ipv4.payload
    protocol = ipv4.proto
    if protocol == 1:
        return ICMP(data)
    if protocol == 6:
        return TCP(data, ipv4.kind, ipv4.getPayloadLength())
    if protocol == 17:
        return UDP(data, ipv4.kind)

def parse(raw_data, iface, mac_addr, ignoreSame):
    eth = EthFrame(raw_data, iface, mac_addr)
    if (ignoreSame and eth.kind == "Loopback") or eth.proto != 8:
        return
    print(eth)
    if eth.proto == 8:
        ipv4 = IPV4(eth.payload, eth.kind)
        print(ipv4)
        parsed_ipv4 = parse_ipv4(ipv4)
        if parsed_ipv4:
            print(parsed_ipv4)
            return parsed_ipv4