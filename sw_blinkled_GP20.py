"""Example for Pico. Turns on the An External LED (GP0)"""
"""Push the Button at pin GP20 (Active LOW)"""

import time
import board
import digitalio

led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

switch = digitalio.DigitalInOut(board.GP20)
switch.direction = digitalio.Direction.INPUT

while True:
    if switch.value:
        led.value = False
    else:
        print(switch.value)
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)
            