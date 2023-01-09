# Serial Communication using PyCharm

Link: https://www.jetbrains.com/pycharm/

## Example 1
PyCharm-->Pi Pico

Addtional Library: pyserial
- PyCharm sends a command to the Pi Pico to do a task through serial.

## Example 2
PyCharm-->Pi Pico

Addtional Library: pyserial
- PyCharm sends a 3 commands (RGB Number), and Pi Pico reads using readline() which is should ending in a newline character (\n)

## Example 3
Pi Pico-->PyCharm

Addirional Library: pyserial, numpy, matplotlib
- Pi Pico sends a Temperature and Humidity data (DHT22) and PyCharm received the data and Plot realtime (Matplotlib).
