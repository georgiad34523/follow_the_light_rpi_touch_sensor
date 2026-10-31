
import time
#for controlling and configuring hardware on Rpi
import board
#library for commincating via I2C protocol
import busio

#library for interfacing with sensor
import adafruit_mpr121
#for randomly picking which led will light up in the sequence
import random

#deque is more optimised than list for popleft, O(1) instead of O(n)
from collections import deque as dq
from gpiozero import LED
import asyncio
import time

#code from the github for the adafruit_mpr121 library, for setup of communication between the sensor and Rpi
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)

#Initialising variables
led_1 = LED(26)
led_2 = LED(12)
led_3 = LED(4)

sequence = dq()
game_over = asyncio.Event()
increment = 0.5
score = 0

#-------------------LED Functions-----------------#
def leds_on():
    led_1.on()
    led_2.on()
    led_3.on()

def leds_off():
    led_1.off()
    led_2.off()
    led_3.off()

async def led_flash(led): 
    '''This function is intended to turn on 
    and off the led from the corresponding random number 
    generated in the sequence'''
    global increment
    if led== 1:
        led_1.on()
        await asyncio.sleep(increment)
        led_1.off()
        await asyncio.sleep(increment)
    if led == 2:
        led_2.on()
        await asyncio.sleep(increment)
        led_2.off()
        await asyncio.sleep(increment)
    if led == 3:
        led_3.on()
        await asyncio.sleep(increment)
        led_3.off()
        await asyncio.sleep(increment)
    increment = max(0.1, increment*0.95)

def leds_flash():
    leds_on()
    time.sleep(0.5)
    leds_off()
    time.sleep(0.5)

def start_end():
    '''ending and starting sequence of the game'''
    leds_flash()
    leds_flash()
    leds_flash()

#---------------Game Logic Functions-----------#
async def generate_sequence():
    '''While the game is running, generates a random number, 
    appends it to the sequence and calls the flash led function'''
    interval = 0.7
    while not game_over.is_set():
        r = random.randint(1,3)
        sequence.append(r)
        await led_flash(r)
        print(sequence)
        interval= max(0.2, interval*0.95)
        await asyncio.sleep(interval)

async def check_tap(next_tap = False):
    '''Checks for sensor input, checks if its a tap or continuing press
    checks this tap against the next number in the generated sequence
    if tap is wrong, flags the game as over.
    if tap is right, updates score'''
    global score
    previous = [False]*4
    while not game_over.is_set():
        for i in range(1,4):
            pressed = bool(mpr121[i].value)
            if pressed:
                print("detected press:", i)
            if pressed and not previous[i]:
                if sequence:
                    next_tap = sequence.popleft()
                    score+=1
                    if i == next_tap:
                        print("correct")
                    else:
                        print("incorrect")
                        game_over.set()
                        break
                else:
                    print("incorrect")
                    game_over.set()
                    break
            previous[i]=pressed
        await asyncio.sleep(0.07)

async def main():
    '''initialises the function that will run the check tap and generate
    sequence functions together, by switching between them
    in the wait periods of each function'''
    await asyncio.gather(generate_sequence(), check_tap())

#-----------------------Run Game----------------------#
start_end()
asyncio.run(main())
start_end()
print("score:", score)
