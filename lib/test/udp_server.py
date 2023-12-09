import socket

server_ip = '10.0.0.1'
server_port = 12462

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

while True:
    data, client_address = server_socket.recvfrom(1024)
    response_message = "Hello, client!" 
    server_socket.sendto(response_message.encode(), client_address)