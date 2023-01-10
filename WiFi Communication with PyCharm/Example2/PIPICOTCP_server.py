# PyCharm: TCP_Server connected with Pi Pico W as Client
# Reference: https://github.com/anecdata/Socket/blob/main/examples/tcp_server_CPython.py

import socket

HOST = ""
PORT = 5000
TIMEOUT = None
MAXBUF = 256

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + IPAddr)

print("Create TCP Server Socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(TIMEOUT)
s.bind((HOST, PORT))
s.listen()
print("Listening")

buf = bytearray(MAXBUF)

while True:
    print("Accepting connections")
    conn, addr = s.accept()
    conn.settimeout(TIMEOUT)
    print("Accepted from", addr)

    buf = conn.recv(MAXBUF)
    print("Received", buf, "from", addr)

    size = conn.sendall(buf)
    print("Sent", buf[:size], size, "bytes to", addr)

    conn.close()
