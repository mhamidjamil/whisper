import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 12345))  # Change port as needed
server_socket.listen(1)
print("Server listening...")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")

try:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Received:", data.decode())
except Exception as e:
    print("Server error:", e)
finally:
    conn.close()
    server_socket.close()
