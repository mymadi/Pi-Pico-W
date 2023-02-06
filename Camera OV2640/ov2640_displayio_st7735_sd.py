"""
1) Display an image from the camera and display it on a:
 - 1.8-inch 128x160 TFT LCD Breakout - ST7735
 
 2) Uncomment
     #     capture_image()
     #     time.sleep(5)
Capture an image from the camera with 5 seconds delay and save to SD Card.
"""
import storage
import sdcardio
import os
import time
import board
import busio
import digitalio
import displayio
from adafruit_st7735r import ST7735R
from displayio import (
    Bitmap,
    Group,
    TileGrid,
    FourWire,
    release_displays,
    ColorConverter,
    Colorspace,
)
import adafruit_ov2640

# Release any resources currently in use for the displays
displayio.release_displays()

# TFT 1.8 LCD -----------------------------------------
spi = busio.SPI(board.GP10,board.GP11,board.GP12)
tft_cs = board.GP13
tft_dc = board.GP15
display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP14
)
display = ST7735R(display_bus, width=160, height=128, rotation=90)
# -----------------------------------------------------

# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus
with digitalio.DigitalInOut(board.GP26) as shutdown:
    shutdown.switch_to_output(True)
    time.sleep(0.001)
    bus = busio.I2C(board.GP21, board.GP20)

# Set up the camera (you must customize this for your board!)
cam = adafruit_ov2640.OV2640(
    bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP8,
    vsync=board.GP9,
    href=board.GP28,
    #mclk=None,
    mclk_frequency=20_000_000,
    shutdown=board.GP26,
    reset=board.GP27,
    size=adafruit_ov2640.OV2640_SIZE_QVGA,
)  # [14]
cam.flip_x = False
cam.flip_y = True
pid = cam.product_id
ver = cam.product_version
print(f"Detected pid={pid:x} ver={ver:x}")
#cam.test_pattern = True

g = displayio.Group(scale=1)
bitmap = displayio.Bitmap(320, 240, 65536)
tg = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.BGR565_SWAPPED
    ),
)

g.append(tg)
display.show(g)
display.auto_refresh = False

# SD Card Storage ------------------------------------
SD_CS = board.GP17                 # Chip Select
#                   CLK         MOSI        MISO
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
#cs = digitalio.DigitalInOut(SD_CS)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

_image_counter = 0

def open_next_image():
    global _image_counter
    while True:
        filename = f"/sd/img{_image_counter:04d}.jpg"
        _image_counter += 1
        if exists(filename):
            continue
        print("#", filename)
        return open(filename, "wb")  # pylint: disable=consider-using-with

def capture_image():
    old_size = cam.size
    old_colorspace = cam.colorspace
    try:
        #cam.size = adafruit_ov2640.OV2640_SIZE_HD
        cam.colorspace = adafruit_ov2640.OV2640_COLOR_JPEG
        b = bytearray(cam.capture_buffer_size)
        jpeg = cam.capture(b)
        
        print(f"Captured {len(jpeg)} bytes of jpeg data")
        with open_next_image() as f:
            f.write(jpeg)        
    finally:
        cam.size = old_size
        cam.colorspace = old_colorspace
#-----------------------------------------------


# t0 = time.monotonic_ns()

while True:
#     capture_image()
#     time.sleep(5)
    cam.capture(bitmap)
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)
#     t1 = time.monotonic_ns()
#     print("fps", 1e9 / (t1 - t0))
#     t0 = t1
cam.deinit()
