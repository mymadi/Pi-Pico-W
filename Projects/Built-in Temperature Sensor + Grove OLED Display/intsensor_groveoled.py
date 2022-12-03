'''
Grove OLED Display with Temperature Internal Sensor
Additional Libraries
    – adafruit_display_text
    – adafruit_displayio_ssd1306.mpy
'''

import time
import board
import busio
import displayio
import terminalio
import microcontroller
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c_oled = busio.I2C(scl=board.GP5, sda=board.GP4)
display_bus = displayio.I2CDisplay(i2c_oled, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

while True:
    # Read the Temperature from Internal Sensor
    data = microcontroller.cpu.temperature
    # Make the display context
    text_group = displayio.Group()
    # Draw a label
    text = "PI PICO W TEMPERATURE"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=4)
    text_group.append(text_area)
    
    text = "Temp (C):   {:.2f}".format(data)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=17)
    text_group.append(text_area)
    
    text = ""
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=30)
    text_group.append(text_area)
    
    text = ""
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=43)
    text_group.append(text_area)

    text = ""
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=56)
    text_group.append(text_area)

    display.show(text_group)

    time.sleep(2)
