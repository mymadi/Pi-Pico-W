# Serial Communication using PyCharm

Python IDE for PC: https://www.jetbrains.com/pycharm/

Python IDE for Pi Pico W: https://thonny.org/

Programming Language: https://circuitpython.org/board/raspberry_pi_pico_w/

Components (Please Check your Port Number at 'Device Manager'):
- USB to serial
- Bluetooth HC05 (Default Password: 0000 or 1234 and Default Baudrate: 9600)

## Example 1
PyCharm<b>--></b>Pi Pico

Additional Library: pyserial
- PyCharm sends a command to the Pi Pico to do a task through serial.

## Example 2
PyCharm<b>--></b>Pi Pico

Additional Library: pyserial
- PyCharm sends a 3 commands (RGB Number), and Pi Pico reads using readline() which is should ending in a newline character (\n)

## Example 3
Pi Pico<b>--></b>PyCharm

Additional Library: pyserial, numpy, matplotlib
- Pi Pico sends a Temperature and Humidity data (DHT22) and PyCharm received the data and Plot realtime (Matplotlib).
