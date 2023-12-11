from lib.parse.eth import EthFrame
from lib.parse.ipv4 import IPV4
from lib.parse.tcp import TCP
from lib.parse.icmp import ICMP
from lib.parse.udp import UDP
from lib.parse.dns import DNS
from lib.parse.dhcp import DHCP
from lib.parse.http import HTTP
from lib.parse.ssh import SSH
from lib.parse.arp import ARP
from lib.parse.ipv6 import IPV6
from lib.parse.icmp6 import ICMP6
from lib.parse.dhcp6 import DHCP6

"""
Processes TCP packets
also handles specific protocols: DNS, HTTP, SSH
"""
def _handle_tcp(data, kind, len, writeSniff):
    tcp = TCP(data, kind, len)
    writeSniff(tcp)
    if 53 in [tcp.src, tcp.dst]:
        dns = DNS(tcp.payload)
        writeSniff(dns)
    elif 80 in [tcp.src, tcp.dst]:
        http = HTTP(tcp.payload)
        writeSniff(http)
    elif 22 in [tcp.src, tcp.dst]:
        ssh = SSH(tcp.payload, tcp.dst)
        writeSniff(ssh)
    else:
        writeSniff(tcp.strPayload())
    return tcp

"""
Handles ICMP packets for IPv4
"""
def _handle_icmp(data, writeSniff):
    icmp = ICMP(data)
    writeSniff(icmp)
    return writeSniff(icmp.strPayload())

"""
Handles ICMPv6 packets for IPv6
"""
def _handle_icmp6(data, writeSniff):
    icmp = ICMP6(data)
    writeSniff(icmp)
    return writeSniff(icmp.strPayload())

"""
Processes UDP packets
also handles specific protocols: DNS, DHCP
"""
def _handle_udp(data, kind, v6, writeSniff):
    udp = UDP(data, kind)
    writeSniff(udp)
    if 53 in [udp.src, udp.dst]:
        dns = DNS(udp.payload)
        writeSniff(dns)
    elif udp.src in [67, 68] or udp.dst in [67, 68]:
        if v6:
            dhcp = DHCP6(udp.payload)
        else:
            dhcp = DHCP(udp.payload)
        writeSniff(dhcp)
    else:
        writeSniff(udp.strPayload())
    return udp

"""
Parses IPv4 packets
"""
def _parse_protocol4(ipv4, writeSniff):
    data = ipv4.payload
    protocol = ipv4.proto
    if protocol == 1:
        return _handle_icmp(data, writeSniff)
    if protocol == 6:
        return _handle_tcp(data, ipv4.kind, ipv4.getPayloadLength(), writeSniff)
    if protocol == 17:
        return _handle_udp(data, ipv4.kind, False, writeSniff)

"""
Parse IPv6 packets
"""
def _parse_protocol6(ipv6, writeSniff):
    data = ipv6.payload
    protocol = ipv6.next_header
    if protocol == 58:
        return _handle_icmp6(data, writeSniff)
    if protocol == 6:
        return _handle_tcp(data, ipv6.kind, ipv6.getPayloadLength(), writeSniff)
    if protocol == 17:
        return _handle_udp(data, ipv6.kind, True, writeSniff)

"""
Parse packets
"""
def parse(raw_data, iface, mac_addr, ignoreSame, writeSniff):
    eth = EthFrame(raw_data, iface, mac_addr)
    if (ignoreSame and eth.kind == "Loopback"):
        return
    writeSniff('\n')
    writeSniff(eth)
    if eth.proto == 2048:
        ipv4 = IPV4(eth.payload, eth.kind)
        writeSniff(ipv4)
        return _parse_protocol4(ipv4, writeSniff)
    if eth.proto == 2054:
        arp = ARP(eth.payload)
        return writeSniff(arp)
    if eth.proto == 34525:
        ipv6 = IPV6(eth.payload, eth.kind)
        writeSniff(ipv6)
        return _parse_protocol6(ipv6, writeSniff)