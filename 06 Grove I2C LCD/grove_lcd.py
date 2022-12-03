'''
Grove I2C LCD
Reference: https://gist.github.com/idriszmy

Additional Library:
    - grove_lcd_i2c.py

'''

import time
import board
import busio
from grove_lcd_i2c import Grove_LCD_I2C

time.sleep(1)

LCD_SCL = board.GP1
LCD_SDA = board.GP0
LCD_ADDR = 0x3e
i2c = busio.I2C(scl=LCD_SCL, sda=LCD_SDA)
lcd = Grove_LCD_I2C(i2c, LCD_ADDR)

lcd.home()
lcd.print("CircuitPython\nGrove I2C LCD")

time.sleep(2)

lcd.clear()
lcd.print("Hello, UniMAP!")

count = 0

while True:
    count += 1
    lcd.cursor_position(0, 1)
    lcd.print(count)
    time.sleep(1)
