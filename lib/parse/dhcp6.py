import struct
def _get_options_dhcpv6(raw_data):
    options = {}
    i = 0
    while i < len(raw_data):
        if i + 4 > len(raw_data):
            break 
        option_code, option_length = struct.unpack('!HH', raw_data[i:i+4])
        option_data = raw_data[i+4:i+4+option_length]
        options[option_code] = option_data
        i += 4 + option_length
    return options

class DHCP6:
    def __init__(self, raw_data):
        self.msg_type = raw_data[0]
        self.transaction_id = raw_data[1:4]
        self.options = _get_options_dhcpv6(raw_data[4:])

    def __str__(self):
        info = '\t - DHCPv6 Packet:\n'
        info += '\t\t - Message Type: {}\n'.format(self.msg_type)
        info += '\t\t - Transaction ID: {}\n'.format(self.transaction_id.hex())
        for option_code, option_data in self.options.items():
            info += '\t\t\t - Option Type: {}, Option Data: {}\n'.format(option_code, option_data)
        return info
