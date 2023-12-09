import struct
import socket
_DNS_RCODE = {
    0: "No Error",
    1: "Format Error",
    2: "Server Failure",
    3: "Name Error",
    4: "Not Implemented",
    5: "Refused",
    6: "YX Domain",
    7: "YX RR Set",
    8: "NX RR Set",
    9: "Not Auth",
    10: "Not Zone"
}

def _parse_name(raw_data, start):
    labels = []
    pos = start
    jumped = False
    max_jumps = 5 
    jumps_performed = 0

    while True:
        length = raw_data[pos]
        if (length & 0xC0) == 0xC0:
            if not jumped:  
                start = pos + 2
            pointer = ((length & 0x3F) << 8) + raw_data[pos + 1]
            pos = pointer
            jumped = True
            jumps_performed += 1
            if jumps_performed > max_jumps:
                raise Exception("Too many pointer jumps in DNS name.")
        else:
            if length == 0:
                break
            pos += 1
            labels.append(raw_data[pos: pos + length])
            pos += length
    return b'.'.join(labels).decode(), (start if jumped else pos + 1)


def _parse_rr(raw_data, start):
        name, pos = _parse_name(raw_data, start)
        rr_type, rr_class, rr_ttl, rr_rdlength = struct.unpack('!HHIH', raw_data[pos:pos+10])
        pos += 10
        rr_addr = None
        if rr_type == 1:
            rr_addr = socket.inet_ntoa(raw_data[pos:pos+4])
            pos += 4
        elif rr_type == 28:
            rr_addr = socket.inet_ntop(socket.AF_INET6, raw_data[pos:pos+16])
            pos += 16
        else:
            pos += rr_rdlength 

        return {'name': name, 'type': rr_type, 'class': rr_class, 'ttl': rr_ttl, 'address': rr_addr}, pos

class DNS:
    def __init__(self, raw_data):
        self.trans_id, self.flags, self.qdcount, self.ancount, \
        self.nscount, self.arcount = struct.unpack('! H H H H H H', raw_data[:12])
        self.qr = (self.flags >> 15) & 0x1
        self.rcode = self.flags & 0xF
        self.questions = []
        self.answers = []
        pos = 12
        for _ in range(self.qdcount):
            qname, pos = _parse_name(raw_data, pos)
            qtype, qclass = struct.unpack('! H H', raw_data[pos:pos+4])
            pos += 4
            self.questions.append((qname, qtype, qclass))
        for _ in range(self.ancount):
            answer, pos = _parse_rr(raw_data, pos)
            self.answers.append(answer)

    def _get_type(self):
        return "Response" if self.qr == 1 else 'Query'
    
    def _get_rcode(self):
        return _DNS_RCODE[self.rcode]
    
    def __str__(self):
        info = '\t - DNS Packet:\n'
        info += '\t\t - Transaction ID: {}, Flags: {}, Type: {}, RCode: {} ({})\n'.format(self.trans_id, self.flags, self._get_type(), self._get_rcode(), self.rcode)
        info += '\t\t - Questions Count: {}\n'.format(self.qdcount)
        for qname, qtype, qclass in self.questions:
            info += '\t\t\t - Name: {}, Type: {}, Class: {}\n'.format(qname, qtype, qclass)
        info += '\t\t - Answers Count: {}\n'.format(self.ancount)
        for answer in self.answers:
            info += '\t\t\t - Name: {}, Type: {}, Class: {}, TTL: {}, Address: {}\n'.format(
                answer['name'], answer['type'], answer['class'], answer['ttl'], answer['address'] or "N/A"
            )
        return info
