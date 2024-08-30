from machine import Pin, SPI
import framebuf
import utime
from epd_2inch7 import *
from epd_gui import *
from image import *

'''define pin conection
2.7inch_EPD    Raspberry Pi Pico
      RST   --->   GP1
      BUSY  --->   GP0
      D/C   --->   GP2
      MOSI  --->   GP7
      CLK   --->   GP6
      CS    --->   GP3
      D1    --->   GP21
      D2    --->   GP20
      K1    --->   GP18
      K2    --->   GP17 
'''
if __name__ == '__main__':
    gui = EPD_GUI()
    print("2.7'' E-Paper for Pico")

    gui.epd.hw_init_fast()
    gui.epd.whitescreen_all_fast(gImage_0)  # Refresh the picture in full screen
    gui.epd.sleep()  # EPD_sleep,Sleep instruction is necessary, please do not delete!!!
    utime.sleep(2)  # delay 2s


    gui.epd.hw_init_fast()  # Electronic paper initialization
    gui.epd.whitescreen_all(gImage_1)  # Refresh the picture in full screen
    gui.epd.sleep()  # EPD_sleep,Sleep instruction is necessary, please do not delete!!!
    utime.sleep(2)  # delay 2s


    class BreakLoop(Exception):
        pass
    gui.epd.hw_init()  # EPD init
    gui.epd.whitescreen_white()
    gui.epd.setramvalue_basemap(gImage_basemap)  # EPD Clear
    try:
        for fen_h in range(6):
            for fen_l in range(10):
                for miao_h in range(6):
                    for miao_l in range(10):
                        gui.epd.dis_part_myself(64, 76, Num[miao_l], 64, 110, Num[miao_h], 64, 150, gImage_numdot,
                                                64, 190, Num[fen_l], 64, 222, Num[fen_h], 32, 64)
                        utime.sleep(0.3)
                        if fen_l == 0 and miao_h == 1 and miao_l == 0:
                            raise BreakLoop()
    except BreakLoop:
        print("out of time show loop")
    gui.epd.hw_init()  # Electronic paper initialization
#portrait
# 0--------->(175)x
# |
# |
# |
# |
# y(263)
    # Drawing
    gui.epd.init_gui_portrait()
    gui.epd.display_clear()
    gui.draw_portrait.fill(WHITE)
    gui.draw_portrait.text("SEENGREAT", 55, 30, BLACK)
    gui.draw_portrait.text("2.7inch E-Paper", 30, 50, BLACK)
    gui.draw_portrait.text("264*176 pixels", 30, 70, BLACK)
    gui.draw_portrait.vline(0, 0, 263, BLACK)
    gui.draw_portrait.hline(0, 0, 175, BLACK)
    gui.draw_portrait.rect(20, 100, 50, 40, BLACK)
    gui.draw_portrait.fill_rect(100, 100, 40, 40, BLACK)
    gui.draw_portrait.rect(30, 170, 90, 60, BLACK)
    gui.draw_portrait.line(30, 170, 119, 229, BLACK)
    gui.draw_portrait.line(30, 229, 119, 170, BLACK)
    gui.epd.whitescreen_all_fast(gui.img_portrait)
    gui.epd.sleep()
    utime.sleep(3)
#landscape
# 0--------->x(263)
# |               
# |              
# |               
# |              
# y(175)        
    gui.epd.init_gui_landscape()    
    gui.draw_landscape.fill(WHITE)
# #     # Point
    gui.draw_landscape.text("SEENGREAT", 80, 20, BLACK)
    gui.draw_landscape.text("2.7inch E-Paper", 60, 40, BLACK)
    gui.draw_landscape.text("264*176 pixels", 60, 60, BLACK)
#     # Line
    gui.draw_landscape.hline(0, 0, 263, BLACK)
    gui.draw_landscape.vline(0, 0, 175, BLACK)
#     # Rectangle
    gui.draw_landscape.rect(20, 100, 50, 40, BLACK)
    gui.draw_landscape.fill_rect(100, 100, 40, 40, BLACK)
    gui.draw_landscape.rect(160, 100, 90, 40, BLACK)
    gui.draw_landscape.line(160, 100, 249, 139, BLACK)
    gui.draw_landscape.line(160, 139, 249, 100, BLACK)
    gui.epd.display_landscape(gui.img_landscape)
    utime.sleep(3)  # 2s
    gui.epd.sleep()  # EPD_DeepSleep, Sleep instruction is necessary, please do not delete!!!
# 
    # Clear screen
    gui.epd.hw_init()  # EPD init  initialization
    gui.epd.display_clear()  # Show all white
    gui.epd.sleep()  # Enter deep sleep, Sleep instruction is necessary, please do not delete!!!
    utime.sleep(2)
    print("end")
