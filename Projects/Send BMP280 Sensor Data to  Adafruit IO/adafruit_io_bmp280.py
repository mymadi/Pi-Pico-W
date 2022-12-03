'''
Pi Pico W with Adafruit IO + BMP280 Sensor

Additional Library:
 - adafruit_bmp280.mpy
 - adafruit_io
 - adafruit_minimqtt
 - adafruit_register
 
References:
[1] https://learn.adafruit.com/pico-w-wifi-with-circuitpython/pico-w-with-adafruit-io
'''

import os
import time
import ssl
import wifi
import socketpool
import microcontroller
import board
import busio
import adafruit_requests
import adafruit_bmp280
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))

aio_username = os.getenv('aio_username')
aio_key = os.getenv('aio_key')

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)
print("connected to io")

#  use Pico W's GP6 for SDA and GP7 for SCL
i2c_sensor = busio.I2C(scl=board.GP7, sda=board.GP6)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c_sensor, address=0x76)

try:
# get feed
    picowTemp_feed = io.get_feed("bmp-280.temperature")
    picowPress_feed = io.get_feed("bmp-280.pressure")
    picowAlt_feed = io.get_feed("bmp-280.altitude")
except AdafruitIO_RequestError:
# if no feed exists, create one
    picowTemp_feed = io.create_new_feed("bmp-280.temperature")
    picowPress_feed = io.create_new_feed("bmp-280.pressure")
    picowAlt_feed = io.create_new_feed("bmp-280.altitude")

#  pack feed names into an array for the loop
feed_names = [picowTemp_feed, picowPress_feed, picowAlt_feed]
print("feeds created")

clock = 300

while True:
    try:
        #  when the clock runs out..
        if clock > 300:
            #  read sensor
            data = [bmp280.temperature, bmp280.pressure, bmp280.altitude]
            #  send sensor data to respective feeds
            for z in range(3):
                io.send_data(feed_names[z]["key"], data[z])
                print("sent %0.1f" % data[z])
                time.sleep(1)
            #  print sensor data to the REPL
            print("Pressure: {:.2f} hPa".format(bmp280.pressure))
            print("Altitude = {:.2f} meters".format(bmp280.altitude))
            print("Temperature = {:.2f} °C".format(bmp280.temperature))
            print()
            time.sleep(1)
            #  reset clock
            clock = 0
        else:
            clock += 1
    # pylint: disable=broad-except
    #  any errors, reset Pico W
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()
    #  delay
    time.sleep(1)
    print(clock)
