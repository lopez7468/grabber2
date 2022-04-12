#tests turning on neopixel with color sensor data
from machine import Pin
from machine import I2C
from tcs34725 import TCS34725
from time import sleep_ms

import time
from neopixel import Neopixel  # https://github.com/blaz-r/pi_pico_neopixel

#color sensor stuff
i2c_bus = I2C(0, sda=Pin(4), scl=Pin(5))
tcs = TCS34725(i2c_bus)



PIN_NEOPIXEL  = const(28)
SM_NEOPIXEL   = const(0)     # which PIO-SM to use

NUM_NEOPIXELS = const(1)     # Neopixel strip only contains one pixel
PIXEL_NUM     = const(0)     #   and it's the 0th one



neo = Neopixel(NUM_NEOPIXELS, SM_NEOPIXEL, PIN_NEOPIXEL, "GRB")


    
rgb = TCS34725.html_rgb(tcs.read('raw'))
print(rgb)
neo = Neopixel(1, 0, 28, "GRB")

neo.brightness(250)
neo.set_pixel(0, rgb)
neo.show()