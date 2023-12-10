import struct
import ipaddress
def _get_ipv6(addr):
    return str(ipaddress.ip_address(addr))

class IPV6:
    def __init__(self, raw_data, kind):
        self.version = (raw_data[0] >> 4)
        self.kind = kind
        self.traffic_class = ((raw_data[0] & 15) << 4) | (raw_data[1] >> 4)
        self.flow_label = ((raw_data[1] & 15) << 16) | (raw_data[2] << 8) | raw_data[3]
        self.payload_length, self.next_header, self.hop_limit, \
            self.src, self.dst = struct.unpack('! 4x H B B 16s 16s', raw_data[:40])
        self.src = _get_ipv6(self.src)
        self.dst = _get_ipv6(self.dst)
        payload_offset = 40 
        while self.next_header not in [6, 17, 58]: 
            hdr_length = 8  
            if self.next_header == 0:
                hdr_length = (raw_data[payload_offset + 1] + 1) * 8
            elif payload_offset + 1 >= len(raw_data):
                self.payload = None
                return
            self.next_header = raw_data[payload_offset]
            payload_offset += hdr_length
            if payload_offset >= len(raw_data):
                self.payload = None
                return
        self.total_len = self.payload_length - (payload_offset - 40)
        self.payload = raw_data[payload_offset:payload_offset + self.payload_length]

    def __str__(self):
        info = '\t - IPv6 Packet:\n'
        info += '\t\t - Version: {}, Traffic Class: {}\n'.format(self.version, self.traffic_class)
        info += '\t\t - Flow Label: {}, Payload Length: {}\n'.format(self.flow_label, self.payload_length)
        info += '\t\t - Next Header: {}\n'.format(self.next_header)
        info += '\t\t - Hop Limit: {}\n'.format(self.hop_limit)
        info += '\t\t - Source: {}, Dest: {}\n'.format(self.src, self.dst)
        return info
    def getPayloadLength(self):
        return self.total_len