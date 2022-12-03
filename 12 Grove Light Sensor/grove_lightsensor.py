'''
Grove Light Sensor

Buy Here:
https://my.cytron.io/p-grove-light-sensor-v1.2
'''

import time
import board
import analogio

ls = analogio.AnalogIn(board.GP27)

def get_voltage(raw):
    return (raw * 3.3) / 65536

while True:
    raw = ls.value
    volts = get_voltage(raw)
    print("raw = {:5d} volts = {:5.2f} light = {:5.2f}".format(raw, volts, raw/(65536-raw)*1000))
    time.sleep(0.5)
