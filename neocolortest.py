
from machine import Pin
from machine import I2C
from tcs34725 import TCS34725
from time import sleep_ms

i2c_bus = I2C(0, sda=Pin(4), scl=Pin(5))
tcs = TCS34725(i2c_bus)

import time
from neopixel import Neopixel  # https://github.com/blaz-r/pi_pico_neopixel

PIN_NEOPIXEL  = const(28)
SM_NEOPIXEL   = const(0)     # which PIO-SM to use

NUM_NEOPIXELS = const(1)     # Neopixel strip only contains one pixel
PIXEL_NUM     = const(0)     #   and it's the 0th one

# color formula: R    G    B 
COLOR_RED    = (255,   0,   0)
COLOR_YELLOW = (255, 150,   0)
COLOR_GREEN  = (  0, 255,   0)
COLOR_BLUE   = (  0,   0, 255)
COLOR_WHITE  = (255, 255, 255)
COLORS = (COLOR_WHITE, COLOR_RED, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE)

BRIGHTNESS_MIN =   1
BRIGHTNESS_MAX = 255

neo = Neopixel(NUM_NEOPIXELS, SM_NEOPIXEL, PIN_NEOPIXEL, "GRB")
"""
while True:
    for i in range(len(COLORS)):
        for br in range(BRIGHTNESS_MIN, BRIGHTNESS_MAX+1):
            neo.brightness(br)
            neo.set_pixel(PIXEL_NUM, COLORS[i])
            neo.show()
            time.sleep(0.01)
    """        
def light_on(duty):
    neo = Neopixel(1, 0, 28, "GRB")
    br = 254 * duty/100
    neo.brightness(br)
    neo.set_pixel(0, (255, 255, 255))
    
    
    neo.show()
    

    
    
rgb = TCS34725.html_rgb(tcs.read('raw'))
print(rgb)
neo = Neopixel(1, 0, 28, "GRB")

neo.brightness(250)
neo.set_pixel(0, rgb)
neo.show()