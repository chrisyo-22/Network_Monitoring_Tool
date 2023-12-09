import struct

def _parse_name(raw_data, start):
    labels = []
    pos = start
    while True:
        length = raw_data[pos]
        if length == 0:
            return '.'.join(labels), pos + 1
        labels.append(raw_data[pos + 1: pos + 1 + length].decode())
        pos += length + 1

class DNS:
    def __init__(self, raw_data):
        self.trans_id, self.flags, self.qdcount, self.ancount, \
        self.nscount, self.arcount = struct.unpack('! H H H H H H', raw_data[:12])
        self.questions = []
        self.answers = []
        self.authorities = []
        self.additional = []

        pos = 12
        for _ in range(self.qdcount):
            qname, pos = _parse_name(raw_data, pos)
            qtype, qclass = struct.unpack('! H H', raw_data[pos:pos+4])
            pos += 4
            self.questions.append((qname, qtype, qclass))

    def __str__(self):
        info = '\t - DNS Packet:\n'
        info += '\t\t - Transaction ID: {}, Flags: {}\n'.format(self.trans_id, self.flags)
        info += '\t\t - Questions: {}\n'.format(self.qdcount)
        for qname, qtype, qclass in self.questions:
            info += '\t\t\t - Name: {}, Type: {}, Class: {}\n'.format(qname, qtype, qclass)
        return info
