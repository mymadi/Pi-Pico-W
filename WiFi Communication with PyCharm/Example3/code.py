'''
Pi Pico W: UDP Client communicate with UDP Server (PyCharm)
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
    print("Create UDP Client socket")
    s = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
    s.settimeout(TIMEOUT)

    size = s.sendto(b"Hello, world", (HOST, PORT))
    print("Sent", size, "bytes")

    size, addr = s.recvfrom_into(buf)
    print("Received", buf[:size], size, "bytes from", addr)

    s.close()

    time.sleep(INTERVAL)
