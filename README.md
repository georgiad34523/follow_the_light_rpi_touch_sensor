# follow_the_light_rpi_touch_sensor
A follow the led game, made with raspberry pi and adafruit's capacitive touch hat.

I used and adapted example code from 'Adafruit_CircuitPython_MPR121'

##To play 
Connect the sensor to Rpi, and wire the LEDS to Rpi's gpio pins, change the LED variables in the code to your own gpio pins.

To install library system-wide (this may be required in some cases):

`sudo pip3 install adafruit-circuitpython-mpr121`

To install in a virtual environment in your current project (I had to do this for my Rpi)

```mkdir project-name && cd project-name
python3 -m venv .venv
source .venv/bin/activate
pip3 install adafruit-circuitpython-mpr121```
