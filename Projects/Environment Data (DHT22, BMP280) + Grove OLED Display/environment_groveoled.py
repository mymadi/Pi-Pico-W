'''
Grove OLED Display with DHT22 and BMP280 Sesnsor
Additional Libraries
    – adafruit_display_text
    – adafruit_displayio_ssd1306.mpy
    - adafruit_bmp280.mpy
    - adafruit_dht.mpy

Reference:
[1] https://image.online-convert.com/convert-to-bmp
'''

import time
import board
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
import adafruit_bmp280
import adafruit_dht
from adafruit_display_text import label

# OLED
displayio.release_displays()
i2c_oled = busio.I2C(scl=board.GP5, sda=board.GP4)
display_bus = displayio.I2CDisplay(i2c_oled, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# BMP280 Sensor
i2c_sensor = busio.I2C(scl=board.GP3, sda=board.GP2)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c_sensor, address=0x76)

# DHT22 Sensor
dht22 = adafruit_dht.DHT22(board.GP7)

# Open the file
with open("/battery.bmp", "rb") as bitmap_file:

    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)

    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(
        bitmap,
        pixel_shader = getattr(
            bitmap,
            'pixel_shader',
            displayio.ColorConverter()
        )
    )

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # Add the Group to the Display
    display.show(group)
    
    print("Done!")
    time.sleep(2)
    
while True:
    # Read the Sensor
    temperature = dht22.temperature
    humidity = dht22.humidity
    pressure = bmp280.pressure
    altitude = bmp280.altitude
    
    # Make the display context
    text_group = displayio.Group()
    # Draw a label
    text = "Environment Data"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=4)
    text_group.append(text_area)
    
    text = "Temp (C):   {:.2f}".format(temperature)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=17)
    text_group.append(text_area)
    
    text = "Humi (%):   {:.2f}".format(humidity)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=30)
    text_group.append(text_area)
    
    text = "Pres (hPa): {:.2f}".format(pressure)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=43)
    text_group.append(text_area)

    text = "Alti (m): {:.2f}".format(altitude)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=56)
    text_group.append(text_area)

    display.show(text_group)
    
    print("Environment Data")
    print("Temp (°C): {:.2f}".format(temperature))
    print("Humi (%): {:.2f}".format(humidity))
    print("Pres (hPa): {:.2f}".format(pressure))
    print("Alti (m): {:.2f}\n".format(altitude))

    time.sleep(2)
