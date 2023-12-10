import struct

_ICMPV6_TYPES = {
    1: 'Destination Unreachable',
    2: 'Packet Too Big',
    3: 'Time Exceeded',
    4: 'Parameter Problem',
    128: 'Echo Request',
    129: 'Echo Reply',
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
        info += '\t\t - ICMPv6 Payload:\n'
        info += '\t\t ' + str(self.payload) + '\n'
        return info