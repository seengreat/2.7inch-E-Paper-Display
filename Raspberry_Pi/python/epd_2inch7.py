# Seengreat 2.7 Inch E-Paper Display demo
# Author(s):Andy Li from Seengreat

import os
import sys
import spidev
import time
from gpiozero import *
import numpy as np
"""the following pin definiting use BCM number"""
PIN_CS     = 8
PIN_DC     = 25
PIN_BUSY   = 24
PIN_RST    = 17
EPD_WIDTH  = 176
EPD_HEIGHT = 264

class EPD_2Inch7():
    def __init__(self):
        # spi init
        self.bus = 0
        self.dev = 0
        self.spi_speed = 8000000
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.dev)
        self.spi.max_speed_hz = self.spi_speed
        self.spi.mode = 0b00
        # gpio init
        self.dc = DigitalOutputDevice( PIN_DC,active_high = True,initial_value =False)#
        self.rst = DigitalOutputDevice( PIN_RST,active_high = True,initial_value =False)#
        
        self.busy = DigitalInputDevice(PIN_BUSY,pull_up=True,active_state=None)
        self.w = EPD_WIDTH
        self.h = EPD_HEIGHT
        
    def write_cmd(self, cmd):
        """write command"""
        self.dc.off()
        self.spi.writebytes([cmd])
        
    def write_data(self, value):
        """write data"""
        self.dc.on()
        self.spi.writebytes([value])
        
    def chkstatus(self):
        while self.busy.value==0: 
            pass


    def reset(self):
        """reset the epd"""
        self.rst.off()
        time.sleep(0.1)
        self.rst.on()
        time.sleep(0.1)
        
    def hw_init(self):
        """epd init..."""
        self.reset()
        self.chkstatus()
        self.write_cmd(0x12)
        self.chkstatus()

    def hw_init_fast(self):
        self.reset()

        self.write_cmd(0x12)  # SWRESET
        self.chkstatus()

        self.write_cmd(0x18)  # Read built-in temperature sensor
        self.write_data(0x80)

        self.write_cmd(0x22)  # Load temperature value
        self.write_data(0xB1)
        self.write_cmd(0x20)
        self.chkstatus()

        self.write_cmd(0x1A)  # Write to temperature register
        self.write_data(0x64)
        self.write_data(0x00)

        self.write_cmd(0x22)  # Load temperature value
        self.write_data(0x91)
        self.write_cmd(0x20)
        self.chkstatus()

    def hw_init_gui(self):
        self.reset()
        self.chkstatus()
        self.write_cmd(0x12)  # SWRESET
        self.chkstatus()
        self.write_cmd(0x01)  # Driver output control 
        self.write_data((EPD_HEIGHT+46-1)%256)
        self.write_data((EPD_HEIGHT+46-1)//256)
        self.write_data(0x00)  # 0x00:Show normal 0x01:Show mirror

        self.write_cmd(0x11)  # data entry mode       
        self.write_data(0x01)
        
        self.write_cmd(0x44)  # set Ram-X address start/end position
        self.write_data(0x00)  # 176//8-1=22
        self.write_data(EPD_WIDTH//8-1)

        self.write_cmd(0x45)  # set Ram-Y address start/end position        
        self.write_data((EPD_HEIGHT-1)%256)
        self.write_data((EPD_HEIGHT-1)//256)
        self.write_data(0x00)  # 0x27-->(295+1)=296
        self.write_data(0x00)

        self.write_cmd(0x3C)  # BorderWavefrom
        self.write_data(0x05)
        
        self.write_cmd(0x18)  # Read built-in temperature sensor
        self.write_data(0x80)

        self.write_cmd(0x4E)  # set RAM x address count to 0
        self.write_data(0x00)
        self.write_cmd(0x4F) # set RAM y address count to 0X199
        self.write_data((EPD_HEIGHT-1)%256)
        self.write_data((EPD_HEIGHT-1)//256)
        self.chkstatus()
        
    def update(self):
        self.write_cmd(0x22)
        self.write_data(0xF7)
        self.write_cmd(0x20)
        self.chkstatus()

    def part_update(self):
        self.write_cmd(0x22)
        self.write_data(0xFF)
        self.write_cmd(0x20)
        self.chkstatus()

    def update_fast(self):
        self.write_cmd(0x22)
        self.write_data(0xC7)
        self.write_cmd(0x20)
        self.chkstatus()
    # display
    def whitescreen_all(self,datas):
        self.write_cmd(0x24) #write RAM for black(0)/white (1)
        for i in range(5808):
            self.write_data(datas[i])
        self.update()

    def whitescreen_all_fast(self, datas):
        self.write_cmd(0x24)
        for i in range(5808):
            self.write_data(datas[i])
        self.update_fast()

    def whitescreen_white(self):
        self.write_cmd(0x24) # write RAM for black(0) / white(1)
        for k in range(5808):
#             for i in range(16):
            self.write_data(0xff)
        self.update()

    def sleep(self):
        self.write_cmd(0x10)
        self.write_data(0x01)
        time.sleep(0.01)

    def setramvalue_basemap(self, datas):
        self.write_cmd(0x24)
        for i in range(5808):
            self.write_data(datas[i])
        self.write_cmd(0x26)
        for i in range(5808):
            self.write_data(datas[i])
        self.update()

    def display_part(self, x, y, datas, part_column, part_line):
        x = x//8
        x_end = x + part_line//8-1

        y_start1 = 0
        y_start2 = y
        if y>=256:
            y_start1 = y_start2//256
            y_start2 = y_start2%256
        y_end1 = 0
        y_end2 = y+part_column -1
        if y_end2>=256:
            y_end1 = y_end2//256
            y_end2 = y_end2%256
        self.reset()
        self.write_cmd(0x3C)
        self.write_data(0x80)

        self.write_cmd(0x44)  # set Ram-X address start/end position
        self.write_data(x)
        self.write_data(x_end)  # 0x0C-->(18+1)*8=200

        self.write_cmd(0x45)  # set Ram-Y address start/end position
        self.write_data(y_start2)
        self.write_data(y_start1)
        self.write_data(y_end2)
        self.write_data(y_end1)

        self.write_cmd(0x4E)
        self.write_data(x)
        self.write_cmd(0x4F)
        self.write_data(y_start2)
        self.write_data(y_start1)

        self.write_cmd(0x24)
        for i in range(part_column*part_line//8):
            self.write_data(datas[i])
        self.part_update()

    def display_clear(self):
        self.write_cmd(0x24)
        for i in range(5808):
#             if i<16:
#                 self.write_data(0x00)
#             else:
#                 self.write_data(0xFF)
            self.write_data(0xFF)
        self.update()

    def dis_part_myself(self, xa, ya, da,
                              xb, yb, db,
                              xc, yc, dc,
                              xd, yd, dd,
                              xe, ye, de, part_column, part_line):
        xa = xa//8
        x_end = xa+part_line//8-1
        y_start1 = 0
        y_start2 = ya - 1
        if ya >= 256:
            y_start1 = y_start2 // 256
            y_start2 = y_start2 % 256
        y_end1 = 0
        y_end2 = ya + part_column - 1
        if y_end2 >= 256:
            y_end1 = y_end2 // 256
            y_end2 = y_end2 % 256
        self.reset()
        self.write_cmd(0x3C)
        self.write_data(0x80)

        self.write_cmd(0x44)  # set Ram-X address start/end position
        self.write_data(xa)
        self.write_data(x_end)  

        self.write_cmd(0x45)  # set Ram-Y address start/end position
        self.write_data(y_start2)
        self.write_data(y_start1)
        self.write_data(y_end2)
        self.write_data(y_end1)

        self.write_cmd(0x4E)
        self.write_data(xa)
        self.write_cmd(0x4F)
        self.write_data(y_start2)
        self.write_data(y_start1)

        self.write_cmd(0x24)
        for i in range(part_column*part_line//8):
            self.write_data(da[i])

        xb = xb//8
        x_end = xb+part_line//8-1
        y_start1 = 0
        y_start2 = yb - 1
        if yb >= 256:
            y_start1 = y_start2 // 256
            y_start2 = y_start2 % 256
        y_end1 = 0
        y_end2 = yb + part_column - 1
        if y_end2 >= 256:
            y_end1 = y_end2 // 256
            y_end2 = y_end2 % 256

        self.write_cmd(0x44)  # set Ram-X address start/end position
        self.write_data(xb)
        self.write_data(x_end)  

        self.write_cmd(0x45)  # set Ram-Y address start/end position
        self.write_data(y_start2)
        self.write_data(y_start1)
        self.write_data(y_end2)
        self.write_data(y_end1)

        self.write_cmd(0x4E)
        self.write_data(xb)
        self.write_cmd(0x4F)
        self.write_data(y_start2)
        self.write_data(y_start1)

        self.write_cmd(0x24)
        for i in range(part_column*part_line//8):
            self.write_data(db[i])

        xc = xc//8
        x_end = xc+part_line//8-1
        y_start1 = 0
        y_start2 = yc - 1
        if yc >= 256:
            y_start1 = y_start2 // 256
            y_start2 = y_start2 % 256
        y_end1 = 0
        y_end2 = yc + part_column - 1
        if y_end2 >= 256:
            y_end1 = y_end2 // 256
            y_end2 = y_end2 % 256

        self.write_cmd(0x44)  # set Ram-X address start/end position
        self.write_data(xc)
        self.write_data(x_end) 

        self.write_cmd(0x45)  # set Ram-Y address start/end position
        self.write_data(y_start2)
        self.write_data(y_start1)
        self.write_data(y_end2)
        self.write_data(y_end1)

        self.write_cmd(0x4E)
        self.write_data(xc)
        self.write_cmd(0x4F)
        self.write_data(y_start2)
        self.write_data(y_start1)

        self.write_cmd(0x24)
        for i in range(part_column*part_line//8):
            self.write_data(dc[i])

        xd = xd//8
        x_end = xd+part_line//8-1
        y_start1 = 0
        y_start2 = yd - 1
        if yd >= 256:
            y_start1 = y_start2 // 256
            y_start2 = y_start2 % 256
        y_end1 = 0
        y_end2 = yd + part_column - 1
        if y_end2 >= 256:
            y_end1 = y_end2 // 256
            y_end2 = y_end2 % 256

        self.write_cmd(0x44)  # set Ram-X address start/end position
        self.write_data(xd)
        self.write_data(x_end)  

        self.write_cmd(0x45)  # set Ram-Y address start/end position
        self.write_data(y_start2)
        self.write_data(y_start1)
        self.write_data(y_end2)
        self.write_data(y_end1)

        self.write_cmd(0x4E)
        self.write_data(xd)
        self.write_cmd(0x4F)
        self.write_data(y_start2)
        self.write_data(y_start1)

        self.write_cmd(0x24)
        for i in range(part_column*part_line//8):
            self.write_data(dd[i])

        xe = xe//8
        x_end = xe+part_line//8-1
        y_start1 = 0
        y_start2 = ye - 1
        if ye >= 256:
            y_start1 = y_start2 // 256
            y_start2 = y_start2 % 256
        y_end1 = 0
        y_end2 = ye + part_column - 1
        if y_end2 >= 256:
            y_end1 = y_end2 // 256
            y_end2 = y_end2 % 256

        self.write_cmd(0x44)  # set Ram-X address start/end position
        self.write_data(xe)
        self.write_data(x_end)  # 0x0C-->(18+1)*8=200

        self.write_cmd(0x45)  # set Ram-Y address start/end position
        self.write_data(y_start2)
        self.write_data(y_start1)
        self.write_data(y_end2)
        self.write_data(y_end1)

        self.write_cmd(0x4E)
        self.write_data(xe)
        self.write_cmd(0x4F)
        self.write_data(y_start2)
        self.write_data(y_start1)

        self.write_cmd(0x24)
        for i in range(part_column*part_line//8):
            self.write_data(de[i])
        self.part_update()

    def display(self, image):
        if self.w%8 == 0:
            width = self.w//8
        else:
            width = self.w//8+1
        height = EPD_HEIGHT
        self.write_cmd(0x24)
        for j in range(height):
            for i in range(width):
               self.write_data(image[i + j * width])
        self.update()
        
    def clean_gpio(self):
        self.dc.close()
        self.rst.close()
        self.busy.close()
        print("close")