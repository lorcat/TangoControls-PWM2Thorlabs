# TangoControls-PWM2Thorlabs
Project featuring the stack involving esp32 controlling Thorlabs LEDD1B T-cube LED and Tango Server for communication.

![Illustration](https://raw.githubusercontent.com/lorcat/TangoControls-PWM2Thorlabs/main/images/pogo_snapshot.png "Setup illustration")

## ESP32 controller part
The setup is as follows: <br/>
Esp32c3 controller has firmware running [micropython](https://micropython.org/download/esp32c3-usb/).
Upon the bootup - the device establishes a connection to a wifi point (DHCP), if the connection is established and 
the GPIO pin 3 is high, the device starts webserver based on [tinyweb](https://github.com/belyalov/tinyweb).

Esp32c3 board can signal with internal LED - blinking red (connection is being established), solid red (connection failed), 
green (WIFI connected), purple-white (web server was stated).

The starting web page served by device may look like:

    P02.2 PWM control device
    PWM values and available channels can be inspected here

    In order to inspect an individual channel and to set its value please use the following guide.

    We can inspect channel value via: http://192.168.0.100/pwm/channel_id
    We can set channel value via: http://191.168.0.100/pwm/channel_id?duty_cycle
    
    Here the [channel_id]  is an integer from the list [2, 4, 12, 13, 18, 19].

    The [duty_cycle] is an integer value in the range (0-1023).

Note that the PWM values may be set from 0 to 1023.


Considering the 192.168.0.100 as the IP of the esp32 device the http://192.168.0.100:8080/pwms will show the full state of the PWM channels in the form of a json string:
    
    {"12": 0, "13": 0, "2": 128, "18": 128, "4": 0, "19": 0}

The state for an individual channel can be retrieved by retrieving http://192.168.0.100:8080/pwm/2

    {"2": 128}

## Tango Server

Tango server has the following self-explanatory layout. It allows setting **http_address** 
and **pwm_channel** as properties and has attributes to control intensity of the PWM (0-255).

![Pogo Setup](https://raw.githubusercontent.com/lorcat/TangoControls-PWM2Thorlabs/main/images/pogo_snapshot.png "Pogo Setup illustration")






