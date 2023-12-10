from parse.eth import EthFrame
from parse.ipv4 import IPV4
from parse.tcp import TCP
from parse.icmp import ICMP
from parse.udp import UDP
from parse.dns import DNS
from parse.dhcp import DHCP
from parse.http import HTTP
from parse.ssh import SSH
from parse.arp import ARP
from parse.ipv6 import IPV6
from parse.icmp6 import ICMP6
from parse.dhcp6 import DHCP6
def _handle_tcp(data, kind, len):
    tcp = TCP(data, kind, len)
    print(tcp)
    if 53 in [tcp.src, tcp.dst]:
        dns = DNS(tcp.payload)
        print(dns)
    if 80 in [tcp.src, tcp.dst]:
        http = HTTP(tcp.payload)
        print(http)
    if 22 in [tcp.src, tcp.dst]:
        ssh = SSH(tcp.payload, tcp.dst)
        print(ssh)
    return tcp

def _handle_icmp(data):
    icmp = ICMP(data)
    return print(icmp)

def _handle_icmp6(data):
    icmp = ICMP6(data)
    return print(icmp)

def _handle_udp(data, kind, v6):
    udp = UDP(data, kind)
    print(udp)
    if 53 in [udp.src, udp.dst]:
        dns = DNS(udp.payload)
        print(dns)
    if udp.src in [67, 68] or udp.dst in [67, 68]:
        if v6:
            dhcp = DHCP6(udp.payload)
        else:
            dhcp = DHCP(udp.payload)
        print(dhcp)
    return udp

def _parse_protocol4(ipv4):
    data = ipv4.payload
    protocol = ipv4.proto
    if protocol == 1:
        return _handle_icmp(data)
    if protocol == 6:
        return _handle_tcp(data, ipv4.kind, ipv4.getPayloadLength())
    if protocol == 17:
        return _handle_udp(data, ipv4.kind, False)

def _parse_protocol6(ipv6):
    data = ipv6.payload
    protocol = ipv6.next_header
    if protocol == 58:
        return _handle_icmp6(data)
    if protocol == 6:
        return _handle_tcp(data, ipv6.kind, ipv6.getPayloadLength())
    if protocol == 17:
        return _handle_udp(data, ipv6.kind, True)

def parse(raw_data, iface, mac_addr, ignoreSame):
    eth = EthFrame(raw_data, iface, mac_addr)
    if (ignoreSame and eth.kind == "Loopback"):
        return
    print(eth)
    if eth.proto == 2048:
        ipv4 = IPV4(eth.payload, eth.kind)
        print(ipv4)
        return _parse_protocol4(ipv4)
    if eth.proto == 2054:
        arp = ARP(eth.payload)
        return print(arp)
    if eth.proto == 34525:
        ipv6 = IPV6(eth.payload, eth.kind)
        print(ipv6)
        return _parse_protocol6(ipv6)