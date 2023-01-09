# MIT license

# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)

#import webrepl
#webrepl.start()

from custom_network import start_network, webserver_started
ip = start_network()
globals().setdefault("ip", ip)

from machine import Pin

# all pins supporting PWM
for el in (2, 4, 19, 18, 12, 13):
    p = Pin(el, Pin.OUT)
    p.value(0)

# use PIN3 as a discriminator
# p3 == 0 - we do not run webserver
# p3 == 1 - we run the webserver
p3 = Pin(3, Pin.IN)
v3 = p3.value()

if ip != "0.0.0.0":
    print("Web server autostartup is allowed: {} & {}".format(ip, bool(v3)))

    if v3 > 0:
        print("Starting webserver")
        webserver_started()

        from rest_api import run
        run()
else:
    print("No IP - no webserver")