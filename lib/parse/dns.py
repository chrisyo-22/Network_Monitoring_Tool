import struct
class DNS:
    def __init__(self, raw_data):
        self.trans_id, self.flags = struct.unpack('! H H', raw_data[:4])
        self.payload = raw_data[4:]
    def __str__(self):
        info = '\t\t - DNS Packet:\n'
        info += '\t\t\t - Transaction ID: {}, Flags: {}\n'.format(self.trans_id, self.flags)
        info += '\t\t\t - DNS Payload:\n'
        info += '\t\t\t ' + str(self.payload) + '\n'
        return info