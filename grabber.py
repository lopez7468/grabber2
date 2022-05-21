# grabber.py


from hcsr04 import HCSR04
from machine import Pin, PWM
from time import sleep_us, sleep
import time
from coloroutput import readcolor

USE_POLLING_EVENTER = False

DEBUG = True  # currently just for tracing state transitions

if USE_POLLING_EVENTER:
    from eventer_1b_polls import Event, Eventer
else:
    from eventer2      import Event, Eventer

PIN_LIGHT = const(16)   # LED nearest BUTTON_GP20

# States of the state machine
STATE_OFF = 0
STATE_SEARCH = 1
STATE_MOVE_TOWARDS = 2
STATE_CHECK_COLOR = 3
STATE_MOVE_TOWARDS_NEXT = 4
STATE_GRAB = 5
STATE_MOVE_BACK = 6

STATE_STR = ('STATE_OFF', 'STATE_SEARCH', 'STATE_MOVE_TOWARDS', 'STATE_CHECK_COLOR', 'STATE_MOVE_TOWARDS_NEXT', 'STATE_GRAB', 'STATE_MOVE_BACK')

#stepper variables
dir1 = Pin(11, Pin.OUT)
step = Pin(10, Pin.OUT)

delay_usecs = 1000
STEPS_PER_REV = 200

#Utrasonic variables
sensor = HCSR04(trigger_pin=17, echo_pin=16)

gp0 = Pin(0, Pin.OUT)

# Consolidate error reporting methods (crash, print, beep, etc.) here
def error(err_string):
    raise Exception(err_string)

#servo variables
PIN_SERVO = const(26)       	# GP26 for servo control signal

FREQ_SERVO = const(50)      	# 50ms

servoPin = PWM(Pin(PIN_SERVO))
servoPin.freq(FREQ_SERVO)

#servo2 variables
"""
this was meant for the servo to close the claw

PIN_SERVO = const(22)       	# GP22 for servo control signal

FREQ_SERVO = const(50)      	# 20ms

servoPin = PWM(Pin(PIN_SERVO))
servoPin.freq(FREQ_SERVO)
"""

#moves servo to set degree
def servo(degrees):

    if degrees > 180: degrees=180
    if degrees < 0: degrees=0
    
    maxDuty=9000
    minDuty=1000

    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)

    servoPin.duty_u16(int(newDuty))
    
    # moves the claw forward one step with the stepper motor and checks if something is within 4 cm
def move():
    gp0.off()
    
    step.on()
    sleep_us(delay_usecs)
    step.off()
    sleep_us(delay_usecs)
    
    distance = sensor.distance_cm()
    if distance <= 4:
        gp0.value(1)
        print('test')
    print(distance)
   
#moves claw back the amount of steps it moved forward
def moveback(step_count):
    dir1.on()
    print('moving back')
    for i in range(stepcount):
        step.on()
        sleep_us(delay_usecs)
        step.off()
        sleep_us(delay_usecs)
        sleep(0.05)
    dir1.off()
    
    
# moves servo and checks if there is something within 50cm
def search(degree):
    print('search')
    gp0.off()
    distance = sensor.distance_cm()
    print(distance)
    servo(degree)
    sleep(0.05)
    
    if distance < 50:
        gp0.value(1)    
        sleep(0.5)
        print("done first")
        
def servo2(close):           
    if degrees > 180: degrees=180
    if degrees < 0: degrees=0
    
    maxDuty=9000
    minDuty=1000

    newDuty=minDuty+(maxDuty-minDuty)*(degrees/180)

    servoPin.duty_u16(int(newDuty))
    
#would have closed the claw
def close_claw():
    servo2()#add number

# Take the current state and the next event, perform the appropriate action(s) and
#   return the next state.  The cross-product of all states and events should
#   be completely covered, and unanticipated combinations should result in a
#   warning/error, as that often indicates a consequential bug in the state machine.

#states with no functions move to next state automatically
def event_process(state, event):
    global duty_powerdown
    global deg
    global stepcount
    if state == STATE_OFF:
        
            if event == Event.ON_PRESS:
                eventer.timer_set(1000, periodic=False)
                deg = 0 
                return STATE_SEARCH
            
            else:
                error("Unrecognized event in STATE_OFF")
                
    elif state == STATE_SEARCH:
        
            if event == Event.TIMER:
                search(deg)
                deg = deg + 1
                eventer.timer_set(100, periodic=False)
                
                return STATE_SEARCH
        
            if event == Event.ON_PRESS:
                return STATE_OFF
            
            if event  == Event.TOOCLOSE:
                eventer.timer_cancel()
                stepcount = 0
                print(deg)
                move()
                eventer.timer_set(50, periodic=False)
                return STATE_MOVE_TOWARDS
            #search function and event
            
            
            else:
                error("Unrecognized event in STATE_ON")
                
    elif state == STATE_MOVE_TOWARDS:
            
            if event == Event.ON_PRESS:
                eventer.timer_cancel()
                readcolor()
                return STATE_CHECK_COLOR#fix
            
            if event == Event.TIMER:
                eventer.timer_set(50, periodic=False)
                move()
                stepcount = stepcount + 1
                return STATE_MOVE_TOWARDS
            
            if event  == Event.TOOCLOSE:
                eventer.timer_cancel()
                readcolor()
                return STATE_CHECK_COLOR
            
            
            else:
                error("Unrecognized event in STATE_ON")
                
    elif state == STATE_CHECK_COLOR:
            
            if event == Event.ON_PRESS:
                return STATE_OFF
            
            if event == Event.YES_PRESS:
                
                moveback(stepcount)
                return STATE_MOVE_BACK
            
            if event == Event.NO_PRESS:
                print('fix this')
                return STATE_GRAB
            
            #check color function
            #yes or no event
            
            else:
                error("Unrecognized event in STATE_ON")
    elif state == STATE_GRAB:
            
            if event == Event.ON_PRESS:
                return STATE_OFF
            #grab function
            
            
            else:
                error("Unrecognized event in STATE_ON")
                
    elif state == STATE_MOVE_BACK:
            
            if event == Event.ON_PRESS:
                return STATE_OFF
            #move back function
            
            else:
                error("Unrecognized event in STATE_ON")

# INITIAL CONDITIONS SETUP
gp0.off()

# NO CHANGES SHOULD NEED TO BE MADE BELOW THIS POINT
# unless you want to *temporarily* add some extra debugging code
#
# Keep checking for events and give them to the state machine
# to process (that is, perform the appropriate action for the
# current state and event, and advance to the next state).
eventer = Eventer()
state = STATE_OFF
if DEBUG: print(STATE_STR[state])

while True:
    if USE_POLLING_EVENTER:
        eventer.update()

    event = eventer.next()
    if event != Event.NONE:
        if DEBUG: print(Event.to_string(event), end="")
        state_new = event_process(state, event)
        if DEBUG: print(" -> "+STATE_STR[state_new])
        state = state_new
