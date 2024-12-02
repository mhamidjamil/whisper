import socket

SERVER_IP = "192.168.1.238"  # Replace with Orange Pi's IP address
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

try:
    client_socket.sendall(b"Hello, Orange Pi!")
except Exception as e:
    print("Client error:", e)
finally:
    client_socket.close()
