'''PWM Output for LED Brightness'''

import time
import pwmio
import board

led = pwmio.PWMOut(board.GP0)

while True:
    for bright in range(0, 65535, 1000):
        led.duty_cycle = bright
        time.sleep(0.01)
        
    for bright in range(65535, 0, -1000):
        led.duty_cycle = bright
        time.sleep(0.02)
