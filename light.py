import machine
from machine import Pin, PWM
import time
import _thread
import ujson

status = "OFF"
current_on = 0
previous_on = 0
pwm_pin = PWM(Pin(4))
pwm_pin.freq(120)
pwm_pin.duty(0)
switch_pin = Pin(5, Pin.IN, Pin.PULL_UP)

def value(duty = None):
    if duty == None:
        return (int)(pwm_pin.duty())
    if duty > 1023: duty = 1023
    if duty < 0: duty = 0
    pwm_pin.duty(duty)

def add(duty):
    value(value() + duty)

def switch(p):
    global status
    # Pin interrupt disabled, because it caused a few more interrupts than expected
    switch_pin.irq(None)

    if status == "OFF":
        _thread.start_new_thread(on,())
    else:
        _thread.start_new_thread(off,())
    
    _thread.start_new_thread(switch_wait, ())

def switch_wait():
    time.sleep(0.1)
    # Pin interrupt enabled after delay
    switch_pin.irq(trigger=Pin.IRQ_FALLING, handler=switch)

def on():
    global status
    global current_on
    status = "ON"
    current_on = time.time()
    _thread.start_new_thread(timeout,())        # Run timeout thread when light is put on
    settings = ujson.load(open("settings.json","r"))
    print("Thread on | ID: " + str(_thread.get_ident()))

    while (value() < (1023*settings["Max"]/100) and status == "ON"):
        add(int(value()/settings["Rise"]/10)+1)
        time.sleep(0.01)

def off():
    global status
    global current_on
    global previous_on
    status = "OFF"
    previous_on += int(time.time() - current_on)
    current_on = 0
    settings = ujson.load(open("settings.json","r"))
    print("Thread off | ID: " + str(_thread.get_ident()))

    while (value() > 0 and status == "OFF"):
        add(-(int(value()/settings["Fall"]/10)+1))
        time.sleep(0.01)

def timeout():
    global status
    settings = ujson.load(open("settings.json","r"))
    if settings["Timeout"] == 0: return

    timeout = time.time() + float(settings["Timeout"]*60)
    print("Thread timeout | ID: " + str(_thread.get_ident()))

    while timeout > time.time():
        time.sleep(0.1)
        if status == "OFF": return

    _thread.start_new_thread(off,())

# Enable pin interrupt after start
switch_pin.irq(trigger=Pin.IRQ_FALLING, handler=switch)