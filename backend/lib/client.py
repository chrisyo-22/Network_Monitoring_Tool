import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    # send 1GB of data
    client_socket.sendall(b'1' * (1024 * 1024 * 1024))

    client_socket.close()

if __name__ == '__main__':
    client_program()