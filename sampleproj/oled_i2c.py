# Code adapted by Alexa Jakob from WiseChip's provided I2C code for the QG-2864KLBEG01 display
# Tests OLED by filling the display, and displaying a picture followed by "hello world"

# Copyright (c) 2021, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


from machine import Pin
from smbus2 import SMBus
import time

# define pins - is there a better way to do this? the machine.Pin package doesn't allow for bidirectional pins
RESET = Pin(9, pin.IN)
SCL = Pin(18, pin.IN)
SDA = Pin(19) # bidirectional

global addr = 120 # OLED device address
global bus = SMBus(1)

# instructions are written to address 64, data to address 0
global ins = 64
global data = 0

# coding for picture
sample = [255,1,1,1,1,1,1,1,1,1,1,1,113,145,113,145,145,113,113,145,113,145,145,113,113,145,113,145,145,113,1,1,
1,1,1,1,1,65,241,65,1,1,129,65,65,65,129,1,65,193,65,65,129,1,65,193,1,193,65,193,65,65,209,1,1,1,65,193,65,65,
129,1,1,1,1,1,1,1,1,129,65,65,193,1,65,193,65,65,129,1,1,1,1,1,1,1,1,129,65,65,193,1,129,65,65,65,129,1,193,65,
193,65,129,1,1,1,1,1,1,1,1,1,1,1,1,1,1,255,255,0,0,0,0,0,0,0,0,0,0,0,0,7,0,1,7,0,0,7,0,1,7,0,0,7,0,1,7,0,0,4,0,
0,0,0,0,0,3,4,0,0,3,4,4,4,3,0,8,15,12,4,3,0,0,3,6,1,6,3,0,4,7,4,0,0,4,7,4,0,7,4,16,16,16,16,16,0,0,3,4,4,4,0,4,
7,4,0,7,4,0,4,0,0,0,0,0,3,4,4,4,0,3,4,4,4,3,0,7,0,7,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,128,128,128,
128,128,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,0,0,0,0,0,128,128,128,0,0,0,0,0,0,0,0,128,128,128,
128,128,128,128,128,0,0,0,128,128,128,128,128,128,0,0,0,0,0,0,0,255,255,0,0,0,3,0,0,0,255,0,0,0,3,0,0,192,32,16,
16,16,16,32,192,0,0,0,16,160,32,16,16,16,16,32,192,0,16,112,144,0,144,112,144,0,208,112,16,0,0,0,16,17,241,0,0,0,
0,0,0,16,160,32,16,16,16,16,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,252,2,1,0,0,0,1,2,252,0,0,0,255,0,0,0,0,0,0,0,0,0,0,
255,32,32,32,32,248,1,2,0,0,0,255,0,0,0,0,1,6,248,0,0,0,0,255,255,0,0,0,0,0,0,16,31,16,0,0,0,0,0,7,8,16,16,16,16,
8,7,0,0,0,128,255,136,16,16,16,16,8,7,0,0,0,7,24,7,0,7,24,7,0,0,0,0,0,16,16,31,16,16,0,0,0,0,16,31,16,0,0,0,16,31,
16,0,128,128,128,128,128,128,128,128,128,128,0,0,3,4,8,16,16,16,8,4,3,0,0,16,31,16,16,16,16,16,24,4,0,0,16,31,16,
16,16,16,16,24,4,0,0,16,31,16,16,16,16,8,6,1,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,64,192,64,64,192,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,128,64,64,128,0,0,64,64,192,64,0,0,192,64,64,64,0,0,192,64,64,64,0,0,0,0,0,0,0,0,128,64,64,
128,0,0,128,64,64,128,0,0,128,64,64,128,0,0,0,128,224,0,0,0,128,64,64,128,0,0,0,128,224,0,0,0,128,64,64,128,0,0,128,
64,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,16,31,18,7,0,0,10,21,21,30,16,0,17,27,21,27,17,
0,0,0,17,0,0,0,0,15,16,16,15,0,0,0,30,1,0,0,0,9,17,17,14,0,0,9,17,17,14,0,1,1,1,1,1,0,0,13,18,18,13,0,0,8,18,18,13,
0,0,13,18,18,13,0,6,5,4,31,4,0,0,1,18,18,15,0,6,5,4,31,4,0,0,1,18,18,15,0,0,24,20,18,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,255,255,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,
128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,
128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,
128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,
128,128,128,128,128,128,128,128,128,128,128,128,128,255]

# helloworld
# generated using Krita according to these instructions: https://create.arduino.cc/projecthub/138689/pixel-art-on-oled-display-7f8697
helloworld = [255,255,3,0,0,0,0,0,0,0,0,0,0,192,255, 255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,
0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,
0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,
255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,
255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,
0,0,192,255,255,255,255,3,0,0,0,0,0,0,240,3,0,0,192,255,255,255,255,3,7,206,255,57,224,0,252,7,0,0,192,255,255,255,255,
3,7,206,255,57,224,0,254,15,0,0,192,255,255,255,255,3,7,206,255,57,224,0,30,30,0,0,192,255,255,255,255,3,7,206,1,56,224,
0,15,60,0,0,192,255,255,255,255,3,7,206,1,56,224,0,7,56,0,0,192,255,255,255,255,3,255,207,255,56,224,128,7,120,0,0,192,
255,255,255,255,3,255,207,255,56,224,128,3,112,0,0,192,255,255,255,255,3,255,207,255,56,224,128,3,112,0,0,192,255,255,
255,255,3,7,206,1,56,224,128,7,120,0,0,192,255,255,255,255,3,7,206,1,56,224,0,7,56,0,0,192,255,255,255,255,3,7,206,1,56,
224,0,15,60,0,0,192,255,255,255,255,3,7,206,255,57,224,0,30,30,0,0,192,255,255,255,255,3,7,206,255,249,239,127,252,15,0,
0,192,255,255,255,255,3,7,206,255,249,239,127,248,7,0,0,192,255,255,255,255,3,0,0,0,0,0,0,240,3,0,0,192,255,255,255,255,
3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,
255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,
255,255,131,3,3,135,31,248,15, 6,248,7,12,192,255,255,255,255,131,7,135,231,127,248, 31,6,248,31,12,192,255,255,255,255,3,
135,135,243,96,24,56,6,56,56,12,192,255,255,255,255,3,199,143,115,224,24,48,6,24,48,12,192,255,255,255,255,3,199,143,59,
192,25,48,6,56,112,12,192,255,255,255,255,3,239,223,59,192,25,48,6,24,96,12,192,255,255,255,255,3,238,220,57,192,249,63,
7,56,96,12,192,255,255,255,255,3,238,220,57,192,249,31,6,24,96,12,192,255,255,255,255,3,238,220,57,192,185,15,6,56,96,12,
192,255,255,255,255,3,236,220,56,192,25,15,6,24,96,12,192,255,255,255,255,3,124,248,48,192,24,30,6,56,112,12,192,255,255,
255,255,3,124,248,112,224,24,60,6,24,48,8,192,255,255,255,255,3,124,248,224,127,56,120,254,59,61,12,192,255,255,255,255,3,
56,112,192,127,24,112,254,251,31,12,192,255,255,255,255,3,16,32,128,31,24,96,254,251,15,8,192,255,255,255,255,3,0,0,0,0,0,
0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,
0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,
0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,
3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,192,255,255,255,
255,3,0,0,0,0,0,0,0,0,0,0,192,255,255]

def setup():
    # resets addresses on display, sets up clocks, and turns on display
    seq = [174, 0, 16, 64, 129, 143, 17, 22, 24, 63, 200, 211, 0,
        213, 128, 217, 34, 218, 18, 219, 64, 141, 20, 175]
    bus.write_i2c_block_data(addr, ins, seq)

def fill(col1, col2):
    # fills portion of screen from column 1 to 2
    set_start()
    bus.write_byte_data(addr, ins, 176) # set page

    for y in range (0, 8):
        set_start()
        newpage = 176 + y
        bus.write_byte_data(addr, ins, newpage)

        for x in range(0, 64):
            bus.write_byte_data(addr, data, col1)
            bus.write_byte_data(addr, data, col2)

def pane():
    # fills certain pane of screen
    set_start()
    bus.write_byte_data(addr, ins, 176) # set page

    for x in range(0,126):
        bus.write_byte_data(addr, data, 1)

    bus.write_byte_data(addr, data, 255)

    set_start()
    bus.write_byte_data(addr, ins, 177) # increment page
    bus.write_byte_data(addr, data, 255)

    for x in range(0, 94):
        bus.write_byte_data(addr, data, 128)
    bus.write_byte_data(addr, data, 255)

def set_start():
    # sets lower and higher column addresses to 0 and 16, respectively
    bus.write_byte_data(addr, ins, 0)   # set lower col start addr
    bus.write_byte_data(addr, ins, 16)  # set higher col start addr

def picture(image):
    # displays a provided picture on every page (8 times), coded as a list of addresses
    i = 0
    set_start()

    for y in range(0,8):
        newpage = 176 + y
        bus.write_byte_data(addr, ins, newpage)
        set_start()

        for x in range(0, 128):
            bus.write_byte_data(addr, data, image[i])
            i += 1

def helloworld(image):
    set_start()
    bus.write_byte_data(addr, ins, 176)

    for i in range(0,8192):
        bus.write_byte_data(addr, data, image[i])

        if i % 1024 == 0:
            newpage = 176 + (i / 1024) # new page number
            bus.write_byte_data(addr, ins, newpage)




if __name__ == "__main__":

    setup()

    fill(255, 255)
    time.sleep(10)

    picture(sample)
    time.sleep(10)

    picture(helloworld)
    time.sleep(10)
else:
    exit

