import struct

_ICMPV6_TYPES = {
    1: 'Destination Unreachable',
    2: 'Packet Too Big',
    3: 'Time Exceeded',
    4: 'Parameter Problem',
    128: 'Echo Request',
    129: 'Echo Reply',
    135: 'Neighbor Solicitation',
    136: 'Neighbor Advertisement',
    139: 'ICMP Node Information Query',
    140: 'ICMP Node Information Response',
    143: 'Version 2 Multicast Listener Report'
}

class ICMP6:
    def __init__(self, raw_data):
        self.type, self.code, self.chksum = struct.unpack('! B B H', raw_data[:4])
        self.payload = raw_data[4:]

    def get_type(self):
        return _ICMPV6_TYPES.get(self.type, "Uncommon Type")

    def __str__(self):
        info = '\t - ICMPv6 Packet:\n'
        info += '\t\t - Type: {} ({}), Code: {}, Checksum: {}\n'.format(self.get_type(), self.type, self.code, self.chksum)
        return info
    
    def strPayload(self):
        info = '\t\t - ICMP Payload:\n'
        info += '\t\t ' + str(self.payload) + '\n'
        return info