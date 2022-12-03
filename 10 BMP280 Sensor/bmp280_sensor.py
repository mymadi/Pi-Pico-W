'''
Read and Display Pressure, Altitude and
Temperature using BMP280 Sensor

Additional Library:
    - adafruit_bmp280.mpy
'''

import time
import board
import busio
import adafruit_bmp280

i2c_sensor = busio.I2C(scl=board.GP7, sda=board.GP6)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c_sensor, address=0x76)

while True:
    print("Pressure: {:.2f} hPa".format(bmp280.pressure))
    print("Altitude = {:.2f} meters".format(bmp280.altitude))
    print("Temperature = {:.2f} °C".format(bmp280.temperature))
    
    time.sleep(2)

