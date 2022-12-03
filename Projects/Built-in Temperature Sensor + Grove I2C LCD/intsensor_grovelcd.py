'''
Read Temperature and Display at
Grove I2C LCD
'''

import time
import board
import busio
import microcontroller
from grove_lcd_i2c import Grove_LCD_I2C

time.sleep(1)

LCD_SCL = board.GP1
LCD_SDA = board.GP0
LCD_ADDR = 0x3e
i2c = busio.I2C(scl=LCD_SCL, sda=LCD_SDA)
lcd = Grove_LCD_I2C(i2c, LCD_ADDR)

lcd.home()
lcd.print("Temperature\nGrove I2C LCD")

time.sleep(2)

lcd.clear()
lcd.print("Temperature:")

while True:
    data = microcontroller.cpu.temperature
    data = "{:.2f}".format(data)
    print("Temperature: ", data, "celcius")
    
    lcd.cursor_position(0, 1)
    lcd.print(data)
    lcd.cursor_position(6, 1)
    lcd.print("C")
    time.sleep(1)

