'''Grove OLED Display'''
# Additional Libraries
# – adafruit_display_text
# – adafruit_displayio_ssd1306.mpy


import time
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c_oled = busio.I2C(scl=board.GP5, sda=board.GP4)
display_bus = displayio.I2CDisplay(i2c_oled, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

while True:
    # Make the display context
    text_group = displayio.Group()
    # Draw a label
    text = ":: Caution ::"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=4)
    text_group.append(text_area)
    
    text = "Highly Additive!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=17)
    text_group.append(text_area)
    
    text = "Hello World!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=30)
    text_group.append(text_area)
    
    text = "UniMAP"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=43)
    text_group.append(text_area)

    text = "mym4d1"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=56)
    text_group.append(text_area)

    display.show(text_group)

    time.sleep(2)
