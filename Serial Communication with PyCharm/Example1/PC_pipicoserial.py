# PyCharm: UART Serial example

# Additional Library
#    - pyserial

import serial
import time

pipico = serial.Serial(port='COM9', timeout=0.1, baudrate=9600)
time.sleep(2)

while True:

    print("Enter '1' to turn 'on' the LED and '0' to turn LED 'off'")

    var = str(input())
    print("You Entered :", var)

    if var == '1':
        pipico.write(str.encode('1'))
        print("LED3 turned on")
        time.sleep(1)

    elif var == '0':
        pipico.write(str.encode('0'))
        print("LED3 turned off")
    elif var == 'a':
        pipico.write(str.encode('a'))
        print("LED2 turned on")
    elif var == 's':
        pipico.write(str.encode('s'))
        print("LED2 turned off")
    elif var == 'b':
        pipico.write(str.encode('b'))
        print("Sounded Buzzer")
