import struct
from datetime import datetime

def _get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

class EthFrame:
    def __init__(self, raw_data, iface, mac_addr):
        self.dst, self.src, self.proto = struct.unpack('! 6s 6s H', raw_data[:14])
        self.payload = raw_data[14:]
        self.dst = _get_mac_addr(self.dst)
        self.src = _get_mac_addr(self.src)
        self.total_len = len(raw_data)
        self.time = str(datetime.now())
        self.iface = iface
        if self.dst == self.src:
            self.kind = "Loopback"
        else:
            self.kind = "Incoming" if self.dst == mac_addr else "Outgoing"
    def __str__(self):
        info = '[{}] Ethernet Frame:\n'.format(self.time)
        info += 'Interface: {}, Total Length: {}\n'.format(self.iface, self.total_len)
        info += 'Source: {}, Dest: {}, Protocol: {}\n'.format(self.src, self.dst, self.proto)
        info += 'Type: {} Packet\n'.format(self.kind)
        return info
