import struct
class TCP:
    def __init__(self, raw_data, kind, length):
        self.src, self.dst, self.seq, self.ack, offset, \
            self.window, self.chksum = struct.unpack('! H H L L H H H', raw_data[:18])
        self.len = (offset >> 12) * 4
        self.bytesize = length - self.len
        self.kind = kind
        self.payload = raw_data[self.len:]
        self.flags = offset
        self.flags = self._get_flags_info()
        self.proto = self._determine_protocol()
    def _determine_protocol(self):
        if self.src == 80 or self.dst == 80:
            return "HTTP"
        if self.src == 443 or self.dst == 443:
            return "HTTPS"
        if self.dst == 53 or self.src == 53:
            return 'DNS'
        if self.dst == 22 or self.src == 22:
            return 'SSH'
        return 'Unknown'
    def _get_flags_info(self):
        flags = []
        if self.flags & 0x001: flags.append("FIN")
        if self.flags & 0x002: flags.append("SYN")
        if self.flags & 0x004: flags.append("RST")
        if self.flags & 0x008: flags.append("PSH")
        if self.flags & 0x010: flags.append("ACK")
        if self.flags & 0x020: flags.append("URG")
        if self.flags & 0x040: flags.append("ECE")
        if self.flags & 0x080: flags.append("CWR")
        if self.flags & 0x100: flags.append("NS")
        return ', '.join(flags)
    def __str__(self):
        info = '\t - TCP Packet:\n'
        info += '\t\t - Source Port: {}, Dest Port: {}, Protocol: {}\n'.format(self.src, self.dst, self.proto)
        info += '\t\t - SeqNumber: {}, ACKNum: {}, Window Size: {}\n'.format(self.seq, self.ack, self.window)
        info += '\t\t - Header Length: {}, Data Size: {} Bytes, Checksum: {}\n'.format(self.len, self.bytesize, self.chksum)
        info += '\t\t - Flags: {}\n'.format(self.flags)
        info += '\t\t - This is an {} packet\n'.format(self.proto)
        return info
    def strPayload(self):
        info = '\t\t - TCP Payload:\n'
        info += '\t\t ' + str(self.payload) + '\n'
        return info
    def getData(self):
        return {'src':self.src, 'dst':self.dst, 'bytes':self.bytesize, 'type': self.kind}