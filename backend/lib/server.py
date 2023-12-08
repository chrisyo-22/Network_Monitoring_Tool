import socket
import time

def server_program():
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host, and a well-known port
    server_socket.bind(('localhost', 5000))

    # become a server socket
    server_socket.listen(1)

    total_data_size = 0
    start_time = time.time()

    while True:
        # establish a connection
        client_socket, addr = server_socket.accept()

        print("Got a connection from %s" % str(addr))
        total_data = []

        while True:
            data = client_socket.recv(8192)
            if data:
                total_data.append(data)
            else:
                end_time = time.time()
                break

        data_size = sum([len(i) for i in total_data])
        total_data_size += data_size
        print('Data size is %s bytes' % data_size)

        elapsed_time = end_time - start_time
        print('Elapsed time is %s seconds' % elapsed_time)

        bandwidth = total_data_size / elapsed_time
        print('Bandwidth is %s bytes/second' % bandwidth)

        client_socket.close()

if __name__ == '__main__':
    server_program()