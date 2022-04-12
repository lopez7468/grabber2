from hcsr04 import HCSR04
import time
from machine import Pin

sensor = HCSR04(trigger_pin=17, echo_pin=16)

gp0 = Pin(0, Pin.OUT)
trigger = Pin(17)
echo = Pin(16)
def move():
    
    distance = sensor.distance_cm()
    """
    if distance < 4:
        gp0.on()
        return True
        """
    print(distance)
   # print(trigger.value())
   # print(echo.value())
while True:

    if move():
        gp0.on()
    
    time.sleep(0.5)