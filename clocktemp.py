# ssk TechCree

from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import time
import machine
import utime
import math
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import machine 
from machine import ADC #Mainboard Sensor
from machine import Pin
import time, random
from machine import Pin, Timer

# Setup Temperaturmessung und Konvertierung
sensor_temp = machine.ADC(4)
#adc = machine.ADC(4) 
conversion_factor = 3.3 / (65535)

# create the rtc object
rtc = machine.RTC()

# create a PicoGraphics framebuffer to draw into
graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)

# create our GalacticUnicorn object
gu = GalacticUnicorn()

#Define some colours
BLACK = graphics.create_pen(0, 0, 0)
RED =  graphics.create_pen(255, 0, 0)
RED2 =  graphics.create_pen(128, 0, 0)
YELLOW = graphics.create_pen(255, 255, 0)
YELLOW2 = graphics.create_pen(100, 100, 0)
GREEN = graphics.create_pen(0, 255, 0)
GREEN2 = graphics.create_pen(0, 128, 0)
CYAN =  graphics.create_pen(0, 255, 255)
BLUE =  graphics.create_pen(0, 0, 255)
BLUE2 =  graphics.create_pen(0, 0, 128)
MAGENTA =  graphics.create_pen(255, 0, 255)
WHITE =  graphics.create_pen(200, 200, 200)
GREY =  graphics.create_pen(100, 100, 100)
DRKGRY =  graphics.create_pen(20, 20, 20)

# Coded small digits
nums =[
    [1,1,1,1,0,1,1,0,1,1,0,1,1,1,1], # 0
    [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0],
    [1,1,1,0,0,1,1,1,1,1,0,0,1,1,1],
    [1,1,1,0,0,1,1,1,1,0,0,1,1,1,1],
    [1,0,0,1,0,1,1,1,1,0,0,1,0,0,1],
    [1,1,1,1,0,0,1,1,1,0,0,1,1,1,1], # 5
    [1,1,1,1,0,0,1,1,1,1,0,1,1,1,1],
    [1,1,1,0,0,1,0,0,1,0,1,0,1,0,0],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1],
    [1,1,1,1,0,1,1,1,1,0,0,1,0,0,1], # 9
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # empty
    [1,1,1,1,0,0,1,0,0,1,0,0,1,1,1] # C
    ]

up_button = machine.Pin(GalacticUnicorn.SWITCH_VOLUME_UP, machine.Pin.IN, machine.Pin.PULL_UP)
down_button = machine.Pin(GalacticUnicorn.SWITCH_VOLUME_DOWN, machine.Pin.IN, machine.Pin.PULL_UP)

def blk():
    graphics.set_pen(BLACK)
    graphics.clear()
    gu.update(graphics)
    

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    #temperature = round(27 - (reading - 0.706) / 0.001721)
    temperature = round(22 - (reading))
    tempa=temperature
    print(tempa) 
    
    def show_digit(dig,xx,yy,c):
        p = 0
        colours = [BLACK,c]
        for row in range(5):
            for col in range(3):
                nn = nums[dig]
                v = nn[p]
                graphics.set_pen(colours[v])
                graphics.pixel(xx+col,yy+row)
                p = p + 1

    def show_number2(val,xx,yy,colour):  #Base 10
        digits = [0,0]
        if val < 100: digits[1] = 0
        digits[0] = val // 10
        if val < 10: digits[1] = 0
        digits[1] = val % 10
        for p in range(2):
            show_digit(digits[p],xx+p*4,yy,colour)

    def blob(xx,yy,r,g,b):               # Small primary rectangle
        t = graphics.create_pen(r,g,b)
        graphics.set_pen(t)    
        for x in range(6):
            for y in range(4):
                graphics.pixel(xx+x,yy +y)           
 
    for i in range(100):
        graphics.set_pen(BLACK)
        graphics.clear()

        year, month, day, wd, hour, minute, second, _ = rtc.datetime()

        show_number2(second,33,0,GREEN2)   # Time
        show_number2(minute,23,0,GREEN2)
        show_number2(hour,13,0,GREEN2)
    
        graphics.set_pen(GREY)          # Colons
        graphics.pixel(21,1)
        graphics.pixel(21,3)
        graphics.pixel(31,1)
        graphics.pixel(31,3)

        #t = int(tempa)
        t = (tempa)
        graphics.set_pen(BLUE)
        show_number2(t,13,6,BLUE)
        show_digit(11,23,6,BLUE)
        graphics.pixel(21,6)
        gu.update(graphics)
        
        if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
            gu.adjust_brightness(+0.01)

        if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            gu.adjust_brightness(-0.01)
        
#Colour mixing
    r = 100 # Start primary colour values
    g = 128
    b = 20

gu.update(graphics)
