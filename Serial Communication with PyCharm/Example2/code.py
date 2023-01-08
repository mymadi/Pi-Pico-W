"""
CircuitPython Essentials UART Serial example using readline
"""

import board
import busio
import time

# UART
uart = busio.UART(board.GP4, board.GP5, timeout=0.1,baudrate=9600)


while True:
    # Read byte from Serial    
    # Read a line, ending in a newline character
    byte_read = uart.readline()     
    if byte_read is not None:
        print(byte_read)
        print(byte_read.decode())
