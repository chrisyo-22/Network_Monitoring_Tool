import struct

def _get_ip(addr):
    return '.'.join(map(str, addr))

class IPV4:
    def __init__(self, raw_data, kind):
        self.ver = raw_data[0] >> 4
        self.len = (raw_data[0] & 0x0F) * 4
        self.total_len, self.ttl, self.proto, self.chksum, self.src, \
        self.dst = struct.unpack('! 2x H 4x B B H 4s 4s', raw_data[:20])
        self.src = _get_ip(self.src)
        self.dst = _get_ip(self.dst)
        self.kind = kind
        self.payload = raw_data[self.len:]
    def __str__(self):
        info = '\t - IPv4 Packet:\n'
        info += '\t\t - Version: {}, Header Length: {}, Total Length: {}\n'.format(self.ver, self.len, self.total_len)
        info += '\t\t - TTL: {}, Protocol: {}, Checksum: {}\n'.format(self.ttl, self.proto, self.chksum)
        info += '\t\t - IP Source: {}, IP Dest: {}\n'.format(self.src, self.dst)
        return info
    def strPayload(self):
        info = '\t\t - IPv4 Payload:\n'
        info += '\t\t ' + str(self.payload) + '\n'
        return info
    def getPayloadLength(self):
        return self.total_len - self.len