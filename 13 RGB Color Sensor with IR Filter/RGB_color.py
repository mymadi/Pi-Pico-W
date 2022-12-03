'''
- Simple demo of the TCS34725 color sensor.
- Will detect the color from the sensor and print it out.
- LED (GP3) will turn off for 3 seconds
'''
import time
import board
import busio
import adafruit_tcs34725
import digitalio


# Create sensor object, communicating over the board's default I2C bus
i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
sensor = adafruit_tcs34725.TCS34725(i2c)

led = digitalio.DigitalInOut(board.GP3)
led.direction = digitalio.Direction.OUTPUT
# Change sensor integration time to values between 2.4 and 614.4 milliseconds
# sensor.integration_time = 150

# Change sensor gain to 1, 4, 16, or 60
# sensor.gain = 4

# Main loop reading color and printing it every second.
while True:
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

    # Read the color temperature and lux of the sensor too.
    temp = sensor.color_temperature
    lux = sensor.lux
    print("Temperature: {0}K Lux: {1}\n".format(temp, lux))
    
    # Delay for turn off LED.
    led.value = False
    time.sleep(3.0)
