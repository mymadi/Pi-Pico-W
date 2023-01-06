"""
CircuitPython Essentials UART Serial example
"""

import board
import busio
import digitalio
import time
import simpleio

# Initialize Input and Output
led3 = digitalio.DigitalInOut(board.GP3)
led2 = digitalio.DigitalInOut(board.GP2)
led3.direction = digitalio.Direction.OUTPUT
led2.direction = digitalio.Direction.OUTPUT
# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18
# UART
uart = busio.UART(board.GP4, board.GP5, timeout=0.1,baudrate=9600)

# Check the LED3
led3.value = True
time.sleep(0.5)
led3.value = False
time.sleep(0.5)
led3.value = True
time.sleep(0.5)
led3.value = False
time.sleep(0.5)

while True:
    # Read byte from Serial
    byte_read = uart.read(1)  # Read one byte over UART lines
    if byte_read == b'1':
        print("LED3 Turn ON")
        led3.value = True
    elif byte_read == b'0':
        print("LED3 Turn OFF")
        led3.value = False
    elif byte_read == b'a':
        print("LED2 Turn ON")
        led2.value = True
    elif byte_read == b's':
        print("LED2 Turn OFF")
        led2.value = False
    elif byte_read == b'b':
        print("Sounded Buzzer")
        simpleio.tone(buzzer, NOTE_C5, duration=0.1)
        # Do Nothing!
        
#     if byte_read is not None:
#         print(byte_read)
