'''
Pi Pico W: Data Collection

Additional libraries
  - simpleio.mpy
  - adafruit_dht.mpy  
'''

import time
import sdcardio
import board
import busio
import digitalio
import storage
import microcontroller
import adafruit_dht
import analogio
import simpleio

# Chip Select
SD_CS = board.GP15

# Connect to the card and mount the filesystem.
#                   CLK         MOSI        MISO
spi = busio.SPI(board.GP10, board.GP11, board.GP12)
#cs = digitalio.DigitalInOut(SD_CS)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Indicator LED
led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

# Buzzer
NOTE_G4 = 392
NOTE_C5 = 523
buzzer = board.GP18

# DHT22
dht22 = adafruit_dht.DHT22(board.GP7)

# LDR
ldr = analogio.AnalogIn(board.GP26)           
R = 10000                       # ohm resistance value

# Read DHT22 Sensor
def readDHT22():
    temperature = dht22.temperature
    humidity = dht22.humidity
    return temperature, humidity

# Read LDR Sensor
def rtolux():
    raw = ldr.value
    vout = (raw * 3.3) / 65536
    RLDR = (vout*R)/(3.3-vout)
    lux = 500/(RLDR/1000)       # Conversion resitance to lumen
    return lux

print("Pi Pico W: Data Collection ^_^")
# append to the file!
while True:    
    # open file for append
    with open("/sd/data01.txt", "a") as f:
        led.value = True  # turn on LED to indicate we're writing to the file
        # Read the Sensors
        dhtval = readDHT22()
        luxval = rtolux()
        temp = round(dhtval[0],2)
        humi = round(dhtval[1],2)
        lux = round(luxval,2)
        temp = microcontroller.cpu.temperature
        
        f.write("{:.2f}, {:.2f}, {:.2f}\n".format(temp,humi,lux))
        led.value = False  # turn off LED to indicate we're done
        simpleio.tone(buzzer, NOTE_G4, duration=0.15)
        
        # Print the Data
        print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH, Lux: {:.2f} lx ".format(temp, humi,lux))

    # file is saved
    time.sleep(5)
