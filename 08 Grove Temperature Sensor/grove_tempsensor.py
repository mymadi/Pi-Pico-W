'''
Grove Temperature Sensor

Buy Here:
https://my.cytron.io/c-sensor/c-temperature-humidity-sensor/p-grove-temperature-sensor
'''
import math
import time
import board
import analogio

gts = analogio.AnalogIn(board.GP27)

B = 4275 # Value for Thermistor
R0 = 100000

def read_sensor():
    raw = gts.value
    R = 65536/raw-1.0
    R = R0*R
    # Convert to temperature via datasheet
    temperature = 1.0/(math.log(R/R0)/B+1/298.15)-273.15;
    return temperature
    
while True:
    temp = read_sensor()
    print("Temp(C) = {:5.2f}".format(temp))
    time.sleep(2)
