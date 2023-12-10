class SSH:
    def __init__(self, raw_data, dst):
        self.direction = 'C2S' if dst == 22 else 'S2C'
        try:
            decoded_data = raw_data.decode('utf-8', errors='ignore')
            if decoded_data.startswith('SSH-'):
                self.handshake = True
                self.details = decoded_data.strip()
            else:
                self.handshake = False
                self.details = "Encrypted SSH or non-handshake data"
        except UnicodeDecodeError:
            self.handshake = False
            self.details = "Encrypted SSH or non-handshake data"

    def __str__(self):
        info = '\t - SSH Protocol:\n'
        direction_str = "client-to-server" if self.direction == 'C2S' else "server-to-client"
        if self.handshake:
            info += '\t\t - Protocol: {}\n'.format(self.details)
        else:
            info += '\t\t - Data: Encrypted or Non-Handshake\n'
        info += '\t\t - Direction: {}\n'.format(direction_str)
        return info