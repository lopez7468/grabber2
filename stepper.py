from machine import Pin
from time import sleep_us, sleep
from hcsr04 import HCSR04

dir1 = Pin(11, Pin.OUT)
step = Pin(10, Pin.OUT)

c = 1000
STEPS_PER_REV = 200

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


step_count = 0
    
def steps(delay_usecs):
    dir1.off()
    step.on()
    sleep_us(delay_usecs)
    step.off()
    sleep_us(delay_usecs)
         
def go_back(step_count, delay_usecs):
    dir1.on()
    for i in range(step_count):
        step.on()
        sleep_us(delay_usecs)
        step.off()
        sleep_us(delay_usecs)
    dir1.off()
    
           

# example usage
while True:
   """ distance = sensor.distance_cm()
    if distance > 4:
        print(sensor.distance_cm())
        print(step_count)
        steps(STEPDELAY_USECS)
        step_count = step_count + 1
        sleep(0.00005)
    if distance < 4:
        print(step_count)
        go_back(step_count, STEPDELAY_USECS)
        break
"""

   for i in range(50):
       
       go_back(1000, 1000)
       sleep(0.005)

