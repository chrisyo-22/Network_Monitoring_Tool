import struct

def _get_ip(addr):
    return '.'.join(map(str, addr))

def _get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

def _get_options(raw_data):
    options = {}
    end = len(raw_data)
    i = 0
    while i < end:
        opt_type = raw_data[i]
        i += 1
        if opt_type == 0 or opt_type == 255:
            continue
        opt_len = raw_data[i]
        i += 1
        opt_data = raw_data[i:i+opt_len]
        i += opt_len
        options[opt_type] = opt_data
    return options

class DHCP:
    def __init__(self, raw_data):
        self.op, self.htype, self.hlen, self.hops, \
        self.xid, self.secs, self.flags, self.ciaddr, \
        self.yiaddr, self.siaddr, self.giaddr, self.chaddr = struct.unpack('! B B B B I H H 4s 4s 4s 4s 16s', raw_data[:44])

        self.ciaddr = _get_ip(self.ciaddr)
        self.yiaddr = _get_ip(self.yiaddr)
        self.siaddr = _get_ip(self.siaddr)
        self.giaddr = _get_ip(self.giaddr)

        self.chaddr = _get_mac_addr(self.chaddr[:self.hlen])
        self.options = _get_options(raw_data[240:])

    def __str__(self):
        info = '\t - DHCP Packet:\n'
        info += '\t\t - Operation: {}, Hardware Type: {}, Hardware Address Length: {}, Hops: {}\n'.format(
            'Boot Request' if self.op == 1 else 'Boot Reply', self.htype, self.hlen, self.hops)
        info += '\t\t - Transaction ID: {}, Seconds elapsed: {}, Flags: {}\n'.format(
            hex(self.xid), self.secs, hex(self.flags))
        info += '\t\t - Client IP Address: {}, Your (client) IP Address: {}\n'.format(
            self.ciaddr, self.yiaddr)
        info += '\t\t - Next Server IP Address: {}, Relay Agent IP Address: {}\n'.format(
            self.siaddr, self.giaddr)
        info += '\t\t - Client MAC Address: {}\n'.format(self.chaddr)
        for opt_type, opt_data in self.options.items():
            info += '\t\t\t - Option Type: {}, Option Data: {}\n'.format(opt_type, opt_data)
        return info