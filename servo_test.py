# photo_pan.py
# value range 29000 - 56000

from machine import Pin, PWM
from time    import sleep

from hcsr04 import HCSR04

sensor = HCSR04(trigger_pin=17, echo_pin=16)






PIN_SERVO = const(22)       	# GP22 for servo control signal

FREQ_SERVO = const(50)      	# 20ms period
servoPin = PWM(Pin(PIN_SERVO))
servoPin.freq(FREQ_SERVO)

def servo(degrees):
    if degrees > 180: degrees=180
    if degrees < 0: degrees=0
    
    maxDuty=9000
    minDuty=1000

    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)

    servoPin.duty_u16(int(newDuty))

while True:
    
    for degree in range(0,180,1):
        if sensor.distance_cm() > 4:
            servo(degree)
            sleep(0.001)
            print("increasing -- "+str(degree))
            print(sensor.distance_cm())
            
        
    for degree in range(180, 0, -1):
        if sensor.distance_cm() > 4:
            servo(degree)
            sleep(0.001)
            print("decreasing -- "+str(degree))
            print(sensor.distance_cm())
    
        
        