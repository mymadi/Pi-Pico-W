# PyCharm: UART Serial example

# Additional Library
#    - pyserial

import serial
import time

pipico = serial.Serial(port='COM9', timeout=0.1, baudrate=9600)
time.sleep(2)

while True:

    print("Enter RGB Color Code")

    r = str(input())
    g = str(input())
    b = str(input())
    print("You Entered (Red) :", r)
    print("You Entered (Green) :", g)
    print("You Entered (Blue) :", b)
    #pipico.write(str.encode(",".join((str(r), str(g), str(b)))))
    rgbtext = str(r) + ' ,' + str(g) + ' ,' + str(b) + ',' + '\n'
    pipico.write(str.encode(rgbtext))
