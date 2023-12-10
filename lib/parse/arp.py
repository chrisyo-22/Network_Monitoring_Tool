import struct

def _get_ip(addr):
    return '.'.join(map(str, addr))

def _get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

class ARP:
    def __init__(self, raw_data):
        self.hardware_type, self.protocol_type, self.hardware_size, \
        self.protocol_size, self.opcode, self.src_mac, \
            self.src_ip, self.dst_mac, self.dst_ip = struct.unpack('! H H B B H 6s 4s 6s 4s', raw_data[:28])
        self.src_mac = _get_mac_addr(self.src_mac)
        self.dst_mac = _get_mac_addr(self.dst_mac)
        self.src_ip = _get_ip(self.src_ip)
        self.dst_ip = _get_ip(self.dst_ip)
        
    def __str__(self):
        opcode_str = "Request" if self.opcode == 1 else "Reply"
        info = '\t - ARP Packet:\n'
        info += '\t\t - Opcode: {}\n'.format(opcode_str)
        info += '\t\t - Hardware Type: {}, Protocol Type: {}\n'.format(self.hardware_type, self.protocol_type)
        info += '\t\t - Source MAC: {}, Source IP: {}\n'.format(self.src_mac, self.src_ip)
        info += '\t\t - Dest MAC: {}, Dest IP: {}\n'.format(self.dst_mac, self.dst_ip)
        return info