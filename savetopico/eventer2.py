# The Eventer class encapsulates all of the event checking and systhesis,
#    away from the state machine implementation code.
#
#
# Written by Eric B. Wertz (eric@edushields.com)
# edited by Antonio to work with our project

import micropython, machine
from machine import Pin, Timer
import hcsr04

micropython.alloc_emergency_exception_buf(100)

class Event():
    """Class enumerating all possible events"""
    
    """No event occurred since last retrieval"""
    NONE  = const(0)

    """On button press occurred"""
    ON_PRESS = const(1)

    """(The) timer expired"""
    TIMER = const(2)
    
    """The yes button (gp21) press occurred"""
    YES_PRESS = const(3)

    """The no button (gp22) press occurred"""
    NO_PRESS = const(4)
    
    """utrasonic sensor got too close"""
    TOOCLOSE = const(5)
    
    def to_string(n):
        return ('NONE', 'ON_PRESS', 'TIMER', 'YES_PRESS', 'NO_PRESS', 'TOOCLOSE')[n]

class TimerInUseException(Exception):
    pass

class Eventer:
    """Custom event manager that composes events from changing conditions in the system
    and queues them up for retrieval, usually from a state machine."""

    PIN_BUTTON = const(20)   # BUTTON_GP20 on baseboard
    PIN21 = const(21)
    PIN22 = const(22)


    def __init__(self):
        """
        Create an event-checker object with an internal list-queue for holding pending events.
        
        params: none
        """
        self.queue = list()

        # Event source: button on PIN_BUTTON
        self.button = Pin(PIN_BUTTON, Pin.IN)        # already pulled-up by resistors on baseboard
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self._isr_button, hard=False)

        # Event source: a single Timer
        self.timer = None
        
        #Event source : button in PIN21
        self.button21 = Pin(PIN21, Pin.IN)        # already pulled-up by resistors on baseboard
        self.button21.irq(trigger=Pin.IRQ_FALLING, handler=self._isr_button21, hard=False)
        
        #Event source : button in PIN22
        self.button22 = Pin(PIN22, Pin.IN)        # already pulled-up by resistors on baseboard
        self.button22.irq(trigger=Pin.IRQ_FALLING, handler=self._isr_button22, hard=False)
        
        #Event source : Utrasonic Sensor getting too close
        #and also triggers when ultrasonic sensor detects something in its sweep
        self.gp0 = Pin(0, Pin.OUT)        # already pulled-up by resistors on baseboard
        self.gp0.irq(trigger=Pin.IRQ_RISING, handler=self._isr_gp0, hard=False)
        
        
    def _isr_gp0(self, pin):
        mask = machine.disable_irq()
        self.queue.append(Event.TOOCLOSE)
        machine.enable_irq(mask)
        
    def _isr_button22(self, pin):
        mask = machine.disable_irq()
        self.queue.append(Event.NO_PRESS)
        machine.enable_irq(mask)
        
    def _isr_button21(self, pin):
        mask = machine.disable_irq()
        self.queue.append(Event.YES_PRESS)
        machine.enable_irq(mask)

    def _isr_button(self, pin):
        mask = machine.disable_irq()
        self.queue.append(Event.ON_PRESS)
        machine.enable_irq(mask)

    def _isr_timer(self, tmr):
        mask = machine.disable_irq()
        self.queue.append(Event.TIMER)
        self.timer = None
        machine.enable_irq(mask)

    def timer_set(self, msecs, periodic=False):
        """Set an (optionally periodic) timer at which time(s) Event.TIMER is generated"""
        if self.timer is None:
            self.timer = Timer(period=msecs,
                               mode=(Timer.PERIODIC if periodic else Timer.ONE_SHOT),
                               callback=self._isr_timer)
        else:
            raise TimerInUseException()
        
    def timer_cancel(self):
        """Cancel the existing timer"""
        if self.timer is not None:
            self.timer.deinit()
            self.timer = None

    def next(self):
        """
        Retrieve the next event (Event.*) from the queue of pending events.
        Returns Event.NONE if no events have occurred since the last call to next().
        
        params: none
        """
        mask = machine.disable_irq()
        e =  self.queue.pop(0) if len(self.queue) else Event.NONE
        machine.enable_irq(mask)

        return e
