import time
import board
import busio
import adafruit_bmp280
import json
import wifi
import socketpool
import os
from adafruit_httpserver import Server, Request, Response, GET
import gc
import adafruit_ntp  # Import NTP library
import rtc

# --- Wi-Fi Configuration ---
WIFI_SSID = "mymadi_2.4G"
WIFI_PASSWORD = "mymadi1234567"  # Your Wi-Fi Password
SERVER_PORT = 5000  # Define the port

print("Connecting to WiFi...")
try:
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    board_ip = wifi.radio.ipv4_address
    print(f"Connected to {WIFI_SSID}! Web server accessible at: http://{board_ip}:{SERVER_PORT}/")
except ConnectionError as e:
    print(f"Failed to connect to WiFi: {e}")
    print("Please check your WIFI_SSID and WIFI_PASSWORD in code.py.")
    while True:
        time.sleep(1)

# --- Initialize NTP Client ---
# Create a socket pool, optionally with a specific DNS server.
# You can try using Google's public DNS servers (8.8.8.8 and 8.8.4.4)
try:
    ntp_pool = socketpool.SocketPool(wifi.radio, dns=("8.8.8.8", "8.8.4.4"))
except TypeError:
    print("TypeError: socketpool.SocketPool doesn't take 'dns' argument.  Proceeding without explicit DNS.")
    ntp_pool = socketpool.SocketPool(wifi.radio) # Fallback without DNS

# Attempt to use a google NTP server
ntp = adafruit_ntp.NTP(ntp_pool, server="time.google.com", tz_offset=-8)

# --- Initialize RTC ---
rtc = rtc.RTC()

# --- Synchronize Time ---
print("Synchronizing time with NTP...")
time.sleep(2)
time_synchronized = False #set to false initially
for _ in range(5):
    try:
        ntp_time = ntp.datetime
        rtc.datetime = ntp_time
        print(f"Time set to: {rtc.datetime}")
        time_synchronized = True
        break
    except AttributeError:
        print("Warning: time.set_time_source not found. Check CircuitPython version (8.x+ recommended).")
        time_synchronized = False
        break
    except Exception as e:
        print(f"Failed to set time: {e}")
        time.sleep(5)

if not time_synchronized:
    print("Warning: Could not synchronize system time via NTP after multiple attempts. Date will be incorrect on graph.")

# --- BMP280 Sensor Setup ---
i2c_sensor = busio.I2C(scl=board.GP9, sda=board.GP8)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c_sensor, address=0x76)

# --- Sensor Data Storage ---
sensor_data_history = {
    "time": [],
    "pressure": [],
    "altitude": [],
    "temperature": []
}
MAX_DATA_POINTS = 50

# --- Web Server Setup ---
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=False, root_path="/") # Removed the port here

# --- Web Server Routes ---
@server.route("/")
def root(request: Request):
    print("Serving index.html")
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return Response(request, html_content, content_type="text/html")
    except OSError as e:
        print(f"Error opening index.html: {e}")
        return Response(request, "Error: index.html not found.", status=500)

@server.route("/data", methods=[GET])
def get_sensor_data(request: Request):
    
    # Convert RTC time to Unix timestamp (milliseconds) for JavaScript
    timestamps = []
    for t in sensor_data_history["time"]:
        if isinstance(t, time.struct_time):
            timestamp_ms = (time.mktime(t)) * 1000 + 8 * 3600 * 1000
        else:
            timestamp_ms = t
        timestamps.append(timestamp_ms)
    
    # Create a new dictionary with the converted timestamps
    response_data = {
        "time": timestamps,
        "pressure": sensor_data_history["pressure"],
        "altitude": sensor_data_history["altitude"],
        "temperature": sensor_data_history["temperature"],
    }
    
    return Response(request, json.dumps(response_data), content_type="application/json")

def start_server(): #added start server function
    try:
        server.start(host=str(wifi.radio.ipv4_address), port=SERVER_PORT)
        print(f"Server started on http://{wifi.radio.ipv4_address}:{SERVER_PORT}") #moved print here
    except OSError as e: #changed to OSError
        if e.errno == 98:  # EADDRINUSE
            print(f"Address already in use.  Trying again in 10 seconds...")
            time.sleep(10)
            start_server()
        else:
            print(f"Failed to start server: {e}")
            time.sleep(10)
            start_server()    # Retry starting the server
    except Exception as e:
        print(f"Exception starting server: {e}")
        time.sleep(10)
        start_server()

# --- Main Loop ---
print(f"Starting web server on port {SERVER_PORT}...")
start_server() #call start server function

last_sensor_read_time = 0
READ_INTERVAL = 2

while True:
    if not wifi.radio.ipv4_address:
        print("WiFi disconnected! Attempting to reconnect...")
        server.stop()
        time.sleep(1)
        try:
            wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
            board_ip = wifi.radio.ipv4_address
            print(f"Reconnected! Web server accessible at: http://{board_ip}:{SERVER_PORT}/")
            start_server()
        except ConnectionError as e:
            print(f"Failed to reconnect to WiFi: {e}")
            time.sleep(5)
            continue
        except Exception as e:
            print(f"Error during WiFi reconnection or server restart: {e}")
            time.sleep(5)
            continue

    try:
        server.poll()
    except Exception as e:
        print(f"Error during server poll: {e}")
        server.stop()
        time.sleep(1)
        start_server()
    current_time = time.monotonic()
    if current_time - last_sensor_read_time >= READ_INTERVAL:
        try:
            pressure = bmp280.pressure
            altitude = bmp280.altitude
            temperature = bmp280.temperature

            # Use RTC time
            current_time_rtc = rtc.datetime
            sensor_data_history["time"].append(current_time_rtc)
            sensor_data_history["pressure"].append(pressure)
            sensor_data_history["altitude"].append(altitude)
            sensor_data_history["temperature"].append(temperature)

            if len(sensor_data_history["time"]) > MAX_DATA_POINTS:
                for key in sensor_data_history:
                    sensor_data_history[key].pop(0)

            print(f"Readings: P: {pressure:.2f} hPa, A: {altitude:.2f} m, T: {temperature:.1f} °C, Time: {current_time_rtc}")

        except RuntimeError as e:
            print(f"Error reading sensor: {e}. Check wiring or sensor!")
        except Exception as e:
            print(f"An unexpected error occurred during sensor read: {e}")

        last_sensor_read_time = current_time

    time.sleep(0.01)
