def _parse_http_headers(message):
    lines = message.split('\r\n')
    start_line = lines[0]
    headers = {}
    for line in lines[1:]:
        if line == '':
            break
        if ': ' in line:
            header_key, header_value = line.split(': ', 1)
            headers[header_key] = header_value
    return start_line, headers

class HTTP:
    def __init__(self, raw_data):
        try:
            self.message = raw_data.decode('utf-8')
            self.start_line, self.headers = _parse_http_headers(self.message)
        except Exception as e:
            print(f"Non HTTP Object: {e}")
            self.start_line = ""
            self.headers = {}

    def __str__(self):
        if self.start_line.strip() == "":
            return ""
        info = '\t - HTTP Message:\n'
        info += '\t\t - {}\n'.format(self.start_line)
        for header, value in self.headers.items():
            info += '\t\t\t - {}: {}\n'.format(header, value)
        return info