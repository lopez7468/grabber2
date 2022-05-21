#function to display oled prompt and color to neopixel
from machine import Pin
from machine import I2C
from tcs34725 import TCS34725
from ssd1306 import SSD1306_I2C
from time import sleep_ms

import time
from neopixel import Neopixel  # https://github.com/blaz-r/pi_pico_neopixel

#color sensor variables
i2c_bus = I2C(0, sda=Pin(4), scl=Pin(5))
tcs = TCS34725(i2c_bus)


#neopixel variables
PIN_NEOPIXEL  = const(28)
SM_NEOPIXEL   = const(0)     # which PIO-SM to use

NUM_NEOPIXELS = const(1)     # Neopixel strip only contains one pixel
PIXEL_NUM     = const(0)     #   and it's the 0th one



neo = Neopixel(NUM_NEOPIXELS, SM_NEOPIXEL, PIN_NEOPIXEL, "GRB")


#oled display variables
PIN_DISP_SCL = const( 7)
PIN_DISP_SDA = const( 6)

I2C_CHANNEL = const(1)
I2C_FREQ    = const(200000)

DISP_WIDTH   = const(128)     # OLED display width
DISP_HEIGHT  = const( 64)     # OLED display height

disp_scl = Pin(PIN_DISP_SCL)
disp_sda = Pin(PIN_DISP_SDA)
i2c = I2C(I2C_CHANNEL, scl=Pin(PIN_DISP_SCL), sda=Pin(PIN_DISP_SDA), freq=200000)
oled = SSD1306_I2C(DISP_WIDTH, DISP_HEIGHT, i2c)

def readcolor():
    #this function makes the color sensor read the color of an object and it uses the rbg value it gets to turn on the neopixel the same color
    #then on the oled display "is this the right color?" is displayed
    rgb = TCS34725.html_rgb(tcs.read('raw'))
    print(rgb)
    neo = Neopixel(1, 0, 28, "GRB")

    neo.brightness(250)
    neo.set_pixel(0, rgb)
    neo.show()
    
    oled.fill(0)                      # clear previous display buffer
    oled.text('  is this the ', 0, 16)
    oled.text('  right color?', 0, 32)
    oled.show() 
