'''
Pi Pico W: TCP Server communicate with TCP Client (PyCharm)
'''
import wifi
import socketpool
import ipaddress
import time
import os

HOST = ""  # see below
PORT = 5000
TIMEOUT = None
BACKLOG = 2
MAXBUF = 256

# Get wifi details from a settings.toml file
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
print("Connecting to WiFi '{}' ... ".format(ssid), end="")
pool = socketpool.SocketPool(wifi.radio)


print("Self IP", wifi.radio.ipv4_address)
HOST = str(wifi.radio.ipv4_address)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
print("Server ping", server_ipv4, wifi.radio.ping(server_ipv4), "ms")

print("Create TCP Server socket", (HOST, PORT))
s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
s.settimeout(TIMEOUT)

s.bind((HOST, PORT))
s.listen(BACKLOG)
print("Listening")

buf = bytearray(MAXBUF)
while True:
    print("Accepting connections")
    conn, addr = s.accept()
    conn.settimeout(TIMEOUT)
    print("Accepted from", addr)

    size = conn.recv_into(buf, MAXBUF)
    print("Received", buf[:size], size, "bytes")

    conn.send(buf[:size])
    print("Sent", buf[:size], size, "bytes")

    conn.close()
