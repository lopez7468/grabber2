# grabber.py
from hcsr04 import HCSR04
from machine import Pin, PWM
import time

USE_POLLING_EVENTER = False

DEBUG = True  # currently just for tracing state transitions

if USE_POLLING_EVENTER:
    from eventer_1b_polls import Event, Eventer
else:
    from eventer2      import Event, Eventer

PIN_LIGHT = const(16)   # LED nearest BUTTON_GP20

# States of the state machine
STATE_OFF = 0
STATE_MOVE_TOWARDS = 1
STATE_GRAB = 2
STATE_MOVE_BACK = 3

STATE_STR = ('STATE_OFF', 'STATE_MOVE_TOWARDS', 'STATE_GRAB', 'STATE_MOVE_BACK')

#Pin Vaiable
light = Pin(PIN_LIGHT)
light_pwm = PWM(light)

#PWm variable
MAX_POWER_OF_2 = const(16)
light_pwm.freq(1000)

#variables to decide powerlevel
DUTY_MAX = const(100)
DUTY_DECR = const( 10) # duty decrement every POWERDOWN_DECR_MSECS
DUTY_MIN = const( 0)

#Utrasonic variables
sensor = HCSR04(trigger_pin=17, echo_pin=16)

gp0 = Pin(0, Pin.OUT)

# Consolidate error reporting methods (crash, print, beep, etc.) here
def error(err_string):
    raise Exception(err_string)


def light_on(duty):
    PWM_OBJ = (2**(16 * duty/100))
    light_pwm.duty_u16(int(PWM_OBJ))
       
def move():
    gp0.off() 
    distance = sensor.distance_cm()
    if distance <= 4:
        gp0.value(1)
        print('test')
    print(distance)
            
            
            
    
        

# Take the current state and the next event, perform the appropriate action(s) and
#   return the next state.  The cross-product of all states and events should
#   be completely covered, and unanticipated combinations should result in a
#   warning/error, as that often indicates a consequential bug in the state machine.
def event_process(state, event):
    global duty_powerdown
    if state == STATE_OFF:
        
            if event == Event.PRESS:
                eventer.timer_set(1000, periodic=False)
                move()
                return STATE_MOVE_TOWARDS
            
            else:
                error("Unrecognized event in STATE_OFF")
                
    elif state == STATE_MOVE_TOWARDS:
            
            if event == Event.PRESS:
                eventer.timer_cancel()
                return STATE_OFF
            
            if event == Event.TIMER:
                eventer.timer_set(500, periodic=False)
                move()
                return STATE_MOVE_TOWARDS
            
            if event  == Event.TOOCLOSE:
                eventer.timer_cancel()
                return STATE_OFF
            
            
            else:
                error("Unrecognized event in STATE_ON")
                
    elif state == STATE_GRAB:
            if event == Event.PRESS:
                return STATE_OFF
            
            
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
