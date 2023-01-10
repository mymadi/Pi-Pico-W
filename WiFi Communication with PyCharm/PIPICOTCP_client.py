# PyCharm: TCP_Client connected with Pi Pico W as Server
# Reference: https://github.com/anecdata/Socket/blob/main/examples/tcp_client_CPython.py

import socket
import time


# edit host and port to match server (Pi Pico W)
HOST = "192.168.0.10"
PORT = 5000
TIMEOUT = 5
INTERVAL = 5
MAXBUF = 256


while True:
    print("Create TCP Client Socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    print("Connecting")
    s.connect((HOST, PORT))

    size = s.send(b'Hello, world')
    print("Sent", size, "bytes")

    buf = s.recv(MAXBUF)
    print('Received', buf)

    s.close()

    time.sleep(INTERVAL)
