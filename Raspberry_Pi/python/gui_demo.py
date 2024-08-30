
from PIL import ImageDraw, Image, ImageFont
import time
from epd_2inch7 import *
from epd_gui import *
from image import *
import gpiozero

'''define pin conection in BCM number
2.7inch_EPD    Raspberry Pi
      VCC   --->   3.3V
      GND   --->   GND
      RST   --->   D17
      BUSY  --->   D24
      D/C   --->   D25
      MOSI  --->   MOSI
      CLK   --->   CLK
      CS    --->   (CE0)D8 
'''
'''
screen coordinates gor gui functions
-----------------> x (0~264)
|
|
|
|
y(0~176)
'''
if __name__ == '__main__':
    gui = EPD_GUI()   
    gui.epd.hw_init_fast()
    gui.epd.whitescreen_all_fast(gImage_0)  # Refresh the picture in full screen
    gui.epd.sleep()  # EPD_sleep,Sleep instruction is necessary, please do not delete!!!
    time.sleep(2)  # delay 2s


    gui.epd.hw_init_fast()  # Electronic paper initialization
    gui.epd.whitescreen_all(gImage_1)  # Refresh the picture in full screen
    gui.epd.sleep()  # EPD_sleep,Sleep instruction is necessary, please do not delete!!!
    time.sleep(2)  # delay 2s


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
                        time.sleep(0.3)
                        if fen_l == 0 and miao_h == 1 and miao_l == 0:
                            raise BreakLoop()
    except BreakLoop:
        print("out of time show loop")
    gui.epd.hw_init()  # Electronic paper initialization
    gui.epd.display_clear()
    # Drawing
    gui.epd.hw_init_gui()  # EPD init
    gui.clear(WHITE)

    font_16 = ImageFont.truetype("MiSans-Light.ttf", FONT_SIZE_16)  # read chinese font file
    font_20 = ImageFont.truetype("MiSans-Light.ttf", FONT_SIZE_20)  # read chinese font file
    font_24 = ImageFont.truetype("MiSans-Light.ttf", FONT_SIZE_24)  # read chinese font file
    font_28 = ImageFont.truetype("MiSans-Light.ttf", FONT_SIZE_28)  # read chinese font file
    # Point
    gui.draw_point(3, 1, BLACK, PIXEL_1X1, DOT_STYLE_DFT)
    gui.draw_point(3, 15, BLACK, PIXEL_2X2, DOT_STYLE_DFT)
    gui.draw_point(5, 40, BLACK, PIXEL_3X3, DOT_STYLE_DFT)
    gui.draw_point(5, 55, BLACK, PIXEL_4X4, DOT_STYLE_DFT)
    # Line
    gui.draw_line(5, 5, 30, 110, BLACK, PIXEL_1X1, LINE_SOLID)
    gui.draw_line(5, 30, 45, 30, BLACK, PIXEL_1X1, LINE_SOLID)
    # Rectangle
    gui.draw_rectangle(20, 5, 95, 80, BLACK, FILL_EMPTY, PIXEL_1X1)
    gui.draw_rectangle(70, 45, 115, 95, BLACK, FILL_FULL, PIXEL_1X1)
    # Circle
    gui.draw_circle(200, 60, 30, BLACK, FILL_EMPTY, PIXEL_1X1)
    gui.draw_circle(226, 75, 18, BLACK, FILL_FULL, PIXEL_1X1)
    gui.draw_str(20, 102, "abcdefg", BLACK, FONT_SIZE_16, font_16)
    gui.draw_str(100,100, "ABCabc012345", BLACK, FONT_SIZE_20, font_20)
    gui.draw_str(40, 120, "2.7\" E-Paper", BLACK, FONT_SIZE_24, font_24)
    gui.draw_str(36, 145, "SEENGREAT", BLACK, FONT_SIZE_28, font_28)
    # TEST_PIN = 1
    gui.epd.display(gui.img)  # display image need 2.08s
    time.sleep(3)  # 2s
    gui.epd.sleep()  # EPD_DeepSleep, Sleep instruction is necessary, please do not delete!!!
# 
# 
#     # Clear screen
    gui.epd.hw_init()  # EPD init  initialization
    gui.epd.display_clear()  # Show all white
    gui.epd.sleep()  # Enter deep sleep, Sleep instruction is necessary, please do not delete!!!
    time.sleep(2)
    print("end")
    gui.epd.clean_gpio()
    exit()
    while True:
        pass
