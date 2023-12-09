import socket
import time

server_ip = '10.0.0.1'
server_port = 12462

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = "Hello, server!"
    client_socket.sendto(message.encode(), (server_ip, server_port))
    time.sleep(10) # send one every 10 seconds