import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = "169.254.88.156"
server_port = 7777
s.bind((server_ip, server_port))
