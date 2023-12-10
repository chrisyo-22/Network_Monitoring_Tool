import struct
_ICMP_TYPES = {
    0: 'Echo Reply',
    3: 'Destination Unreachable',
    4: 'Source Quench',
    5: 'Redirect Message',
    8: 'Echo Request',
    9: 'Router Advertisement',
    10: 'Router Solicitation',
    11: 'Time Exceeded',
    12: 'Parameter Problem',
    13: 'Timestamp',
    14: 'Timestamp Reply',
    15: 'Information Request',
    16: 'Information Reply',
    17: 'Address Mask Request',
    18: 'Address Mask Reply'
}
class ICMP:
    def __init__(self, raw_data):
        self.itype, self.code, self.chksum = struct.unpack('! B B H', raw_data[:4])
        self.payload = raw_data[4:]

    def getType(self):
        return _ICMP_TYPES.get(self.itype, "Uncommon Type")
    
    def __str__(self):
        info = '\t - ICMP Packet:\n'
        info += '\t\t - Type: {} ({}), Code: {}, Checksum: {}\n'.format(self.getType(), self.itype, self.code, self.chksum)
        return info
    
    def strPayload(self):
        info = '\t\t - ICMP Payload:\n'
        info += '\t\t ' + str(self.payload) + '\n'
        return info
