from parse.eth import EthFrame
from parse.ipv4 import IPV4
from parse.tcp import TCP
from parse.icmp import ICMP
from parse.udp import UDP
from parse.dns import DNS

def _handle_tcp(data, kind, len):
    tcp = TCP(data, kind, len)
    print(tcp)
    if(53 in [tcp.src, tcp.dst]):
        dns = DNS(tcp.payload)
        print(dns)
    return tcp

def _handle_icmp(data):
    icmp = ICMP(data)
    return print(icmp)

def _handle_udp(data, kind):
    udp = UDP(data, kind)
    print(udp)
    if(53 in [udp.src, udp.dst]):
        dns = DNS(udp.payload)
        print(dns)
    return udp

def _parse_protocol(ipv4):
    data = ipv4.payload
    protocol = ipv4.proto
    if protocol == 1:
        return _handle_icmp(data)
    if protocol == 6:
        return _handle_tcp(data, ipv4.kind, ipv4.getPayloadLength())
    if protocol == 17:
        return _handle_udp(data, ipv4.kind)

def parse(raw_data, iface, mac_addr, ignoreSame):
    eth = EthFrame(raw_data, iface, mac_addr)
    if (ignoreSame and eth.kind == "Loopback"):
        return
    print(eth)
    if eth.proto == 8:
        ipv4 = IPV4(eth.payload, eth.kind)
        print(ipv4)
        return _parse_protocol(ipv4)
    if eth.proto == 34525:
        print("Ipv6")