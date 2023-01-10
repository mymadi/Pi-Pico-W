# PyCharm: UDP_Server connected with Pi Pico W as Client
# Reference: https://github.com/anecdata/Socket/blob/main/examples/udp_server_CPython.py

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
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(TIMEOUT)
s.bind((HOST, PORT))

buf = bytearray(MAXBUF)

while True:
    size, addr = s.recvfrom_into(buf)
    print("Received", buf[:size], size, "bytes from", addr)

    size = s.sendto(buf[:size], addr)
    print("Sent", buf[:size], size, "bytes to", addr)
