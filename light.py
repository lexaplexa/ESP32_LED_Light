from machine import Pin, PWM
import time
import _thread
import ujson

on_running = False
off_running = False
status = "OFF"
pwm_pin = PWM(Pin(2))
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
    if pwm_pin.duty() == 0:
        _thread.start_new_thread(on,())
    else:
        _thread.start_new_thread(off,())

def on():
    global on_running
    global off_running
    global status

    status = "ON"
    off_running = False
    on_running = True
    _thread.start_new_thread(timeout,())        # Run timeout thread when light is put on
    settings = ujson.load(open("settings.json","r"))

    while (value() < (1023*settings["Max"]/100) and on_running == True):
        add(int(value()/settings["Rise"]/10)+1)
        time.sleep(0.01)

def off():
    global off_running
    global on_running
    global status

    status = "OFF"
    on_running = False
    off_running = True
    settings = ujson.load(open("settings.json","r"))

    while (value() > 0 and off_running == True):
        add(-(int(value()/settings["Fall"]/10)+1))
        time.sleep(0.01)

def timeout():
    global status
    settings = ujson.load(open("settings.json","r"))
    delay_ms = 0

    if settings["Timeout"] == 0: return

    # Timeout is in minutes
    while delay_ms < (settings["Timeout"]*60*1000):
        time.sleep(0.1)
        delay_ms += 100
        if status == "OFF": return

    _thread.start_new_thread(off,())

switch_pin.irq(trigger=Pin.IRQ_FALLING, handler=switch)