# MIT license

import network

from machine import Pin, reset_cause, SOFT_RESET
from neopixel  import NeoPixel 

from time import sleep_ms, time

# Network parameters
SSID = "TP-LINK_4B2C32"
PASS = "77777777"
WLAN = None

LED = None

def set_led(led, state, delay=0, blink=False, off_state=None):
    """
    Sets the main led to a correct state
    """
    if delay > 0:
        sleep_ms(delay)

    led[0] = state
    led.write()

    if blink and off_state:
        if delay > 0:
            sleep_ms(delay)
        led[0] = off_state
        led.write()

def start_network():
    """
    Starts network connection
    """
    global SSID
    global PASS
    global WLAN
    global LED

    res = "0.0.0.0"

    print("Starting connection to {}:{}".format(SSID, PASS))

    WLAN = wlan = network.WLAN(network.STA_IF)

    if not wlan.active():
        print("Wlan is not not active, starting it.")
        wlan.active(True)

        # pins + LED - color pin
        pin = Pin(8, Pin.OUT)
        LED = led = NeoPixel(pin, 1)

        on_red = (20, 0, 0)
        on_green = (0, 20, 0)
        off = (0, 0, 0)

        if reset_cause() != SOFT_RESET:
            # configuration below MUST match your home router settings!!
            # wlan.ifconfig(('192.168.0.200', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
            pass

        if not wlan.isconnected():
            # start connection and do it for 3 times
            for i in range(3):

                if not wlan.isconnected():
                    wlan.connect(SSID, PASS)

                ts = time()

                while not wlan.isconnected() and time()-ts < 3.:
                    set_led(led, on_red, delay=250, blink=True, off_state=off)
                    
                if wlan.isconnected():
                    set_led(led, on_green, delay=200)
                    print("Network Config: {}".format(wlan.ifconfig()))
                    res = wlan.ifconfig()[0]
                    break
                else:
                    set_led(led, on_red)
    return res

def stop_network():
    """
    Stops wlan, switches off the main led to RED
    """
    global WLAN
    global LED 

    if WLAN:
        WLAN.active(False)
        WLAN = None

    if LED:
        LED[0] = (20,0,0)
        LED.write()

def webserver_started():
    """
    Indicates startup of the webserver
    """
    global LED
    if LED:
        LED[0] = (22, 16, 22)
        LED.write()