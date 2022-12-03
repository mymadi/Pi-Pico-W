'''
Color Identification using Adafruit Color Sensor with IR Filter (TCS34725)
Buy Here: https://my.cytron.io/p-rgb-color-sensor-with-ir-filter

Additional Library:
    - adafruit_tcs34725.mpy
    - adafruit_rgbled.mpy
    
References:
[1] https://www.rapidtables.com/web/color/RGB_Color.html
'''

import time
import board
import busio
import adafruit_tcs34725
import adafruit_rgbled
import digitalio

# Create a RGB LED object 
RED_LED = board.GP0
GREEN_LED = board.GP1
BLUE_LED = board.GP2
# invert_pwm=True = for Common Anode
# invert_pwm=False = for Common Cathode
ledRGB = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED, invert_pwm=True)

# Create sensor object, communicating over the board's default I2C bus
i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
sensor = adafruit_tcs34725.TCS34725(i2c)

led = digitalio.DigitalInOut(board.GP3)
led.direction = digitalio.Direction.OUTPUT
sw = digitalio.DigitalInOut(board.GP20)
sw.direction = digitalio.Direction.INPUT
# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

# Main loop reading color and printing it every second.
while True:
    if (sw.value == False):
        
        # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
        # print(sensor.color_raw)
        led.value = True
        time.sleep(2.0)
        color = sensor.color
        color_rgb = sensor.color_rgb_bytes
        print(
            "RGB color as 8 bits per channel int: #{0:02X} or as 3-tuple: {1}".format(
                color, color_rgb
            )
        )
        #ledRGB.color = color
        ledRGB.color = color_rgb
        time.sleep(3.0)
    else:
        led.value = False
