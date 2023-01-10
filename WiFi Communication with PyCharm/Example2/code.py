'''
Pi Pico W: TCP Client communicate with TCP Server (PyCharm)
'''
import wifi
import socketpool
import ipaddress
import time
import os

# edit host and port to match server
HOST = "192.168.0.4"
PORT = 5000
TIMEOUT = 5
INTERVAL = 5
MAXBUF = 256

# Get wifi details from a settings.toml file
print(os.getenv("test_env_file"))
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
print("Connecting to WiFi '{}' ... ".format(ssid), end="")
pool = socketpool.SocketPool(wifi.radio)

print("Self IP", wifi.radio.ipv4_address)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
print("Server ping", server_ipv4, wifi.radio.ping(server_ipv4), "ms")

buf = bytearray(MAXBUF)

while True:
    print("Create TCP Client Socket")
    s = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    print("Connecting")
    s.connect((HOST, PORT))

    size = s.send(b'Hello, world')
    print("Sent", size, "bytes")

    size = s.recv_into(buf)
    print('Received', size, "bytes", buf[:size])

    s.close()

    time.sleep(INTERVAL)
