# MIT license

#!/usr/bin/env micropython
"""
MIT license
(C) Konstantin Belyalov 2017-2018

adjusted by K. Glazyrin <konstantin.glazyrin at desy.de> on 2022/12
Script sets a tinyweb server to control output of the esp32c3 PWM channels [2, 4, 12, 13, 18, 19]
"""

import re
import time

import network
from machine import Pin, PWM

import tinyweb

# global dict for PWMs
PWMS = dict()

# list of esp32c3 pwm channels
PINS = [2, 4, 12, 13, 18, 19]


# main page
MAIN_PAGE = """
<html><head><title>P02.2 PWM control</title>
</head><body>
<h1>P02.2 PWM control device </h1>
<div class='wrapper'>
    <div class='container'>
    <p>PWM values and available channels can be inspected <a href='/pwms'> here</a> </p>
    <p>In order to inspect an individual channel and to set its value please use the following guide.</p>
    <pre>
    We can inspect channel value via: http://{}/pwm/channel_id
    We can set channel value via: http://{}/pwm/channel_id?duty_cycle
    
    Here the [channel_id]  is an integer from the list {}.<br/>
    The [duty_cycle] is an integer value in the range (0-1023).
    </pre>
    </div>
</div>
</body></html>
"""

def prep_pwms():
    """
    Prepares PWM channels and sets them all to 0 duty cycle
    """
    global PWMS
    global PINS

    print("Preparing PWM objects")
    for pin in PINS:
        print("Setting up {}".format(pin))
        PWMS.setdefault(pin, PWM(Pin(pin, Pin.OUT), freq=2000, duty=0))
        time.sleep_ms(200)

def get_pwms():
    """Returns PWMS object for debugging purposes"""
    global PWMS
    return PWMS

class HttpPWMStatus():
    """
    Class returning the data for the pins state
    """
    def get(self, data):
        data = {}

        global PINS
        global PWMS

        ts = time.time()

        [data.setdefault(pin, PWMS[pin].duty()) for pin in PINS]

        return data

class HttpPWM():
    """
    Class setting pwm state of devices
    """
    MAX_DUTY = 1023
    MIN_DUTY = 0

    def not_found(self, id):
        return {'message': 'no such pwm_id ({})'.format(id)}, 404

    def get(self, data, pwm_id):
        """
        Retrieves pwm channel data or an error
        """
        global PWMS

        duty = None
        for k in data.keys():
            if len(k) > 0:
                try:
                    duty = int(k)
                    break
                except ValueError:
                    pass

        try:
            tpwm = int(pwm_id)
            if not tpwm in PWMS:
                raise ValueError

            if isinstance(duty, int) and (self.MIN_DUTY <= duty <= self.MAX_DUTY):
                PWMS[tpwm].duty(duty)
                return {pwm_id: duty}
            else:
                return {pwm_id: PWMS[tpwm].duty()}

        except ValueError:
            return self.not_found(pwm_id)

def run():
    # prepare PWMs
    prep_pwms()

    # Create web server application
    app = tinyweb.webserver()

    # Root page - shows current state, basic info
    @app.route('/')
    async def index(request, response):
        global MAIN_PAGE
        global PINS

        print("Received request for /")

        wlan = network.WLAN(network.STA_IF)
        ip = wlan.ifconfig()[0]

        page = MAIN_PAGE.format(ip, ip, PINS)
        await response.start_html()
        await response.send(page)

    # shows current pwm values as json string
    app.add_resource(HttpPWMStatus, "/pwms")

    # sets values for a pwm
    app.add_resource(HttpPWM, "/pwm/<pwm_id>")

    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    run()
