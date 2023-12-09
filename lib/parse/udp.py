import struct
class UDP:
    def __init__(self, raw_data, kind):
        self.src, self.dst, self.len, self.chksum = struct.unpack('! H H H H', raw_data[:8])
        self.bytesize = self.len - 8
        self.payload = raw_data[8:]
        self.kind = kind
    def __str__(self):
        info = '\t - UDP Packet:\n'
        info += '\t\t - Source Port: {}, Dest Port: {}\n'.format(self.src, self.dst)
        info += '\t\t - Header Length: {}, Data Size: {} Bytes, Checksum: {}\n'.format(self.len, self.bytesize, self.chksum)
        return info
    def strPayload(self):
        info = '\t\t - UDP Payload:\n'
        info += '\t\t ' + str(self.payload) + '\n'
        return info
    def getData(self):
        return {'src':self.src, 'dst':self.dst, 'bytes':self.bytesize, 'type': self.kind}