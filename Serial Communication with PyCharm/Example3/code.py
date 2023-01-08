"""
CircuitPython Essentials UART Serial example
"""

import board
import busio
import digitalio
import time
import simpleio
import os

import adafruit_dht
dht22 = adafruit_dht.DHT22(board.GP7)

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
uart = busio.UART(board.GP4, board.GP5,baudrate=115200)

# Check the LED3
led3.value = True
time.sleep(0.5)
led3.value = False
time.sleep(0.5)
led3.value = True
time.sleep(0.5)
led3.value = False
time.sleep(0.5)
simpleio.tone(buzzer, NOTE_G4, duration=0.1)

while True:
    temperature = dht22.temperature
    humidity = dht22.humidity
    print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH ".format(temperature, humidity))
    humi = str(humidity)
    temp = str(temperature)
    uart.write(str.encode(temp)+','+str(humi)+'\n')
    #uart.write(str.encode(temp)+'\n')

    time.sleep(2)
