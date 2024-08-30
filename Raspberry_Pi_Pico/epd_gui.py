import framebuf
from epd_2inch7 import *

FILL_EMPTY = 0
FILL_FULL = 1

LINE_SOLID = 0
LINE_DOTTED = 1
FONT_SIZE_16 = 16
FONT_SIZE_20 = 20
FONT_SIZE_24 = 24
FONT_SIZE_28 = 28

PIXEL_1X1 = 1  # 1x1
PIXEL_2X2 = 2  # 2X2
PIXEL_3X3 = 3  # 3X3
PIXEL_4X4 = 4  # 4X4
PIXEL_5X5 = 5  # 5X5
PIXEL_6X6 = 6  # 6X6
PIXEL_7X7 = 7  # 7X7
PIXEL_8X8 = 8  # 8X8
DOT_PIXEL_DFT = PIXEL_1X1

WHITE = 0xFF
BLACK = 0x00
RED = BLACK
IMAGE_BACKGROUND = WHITE
FONT_FOREGROUND = BLACK
FONT_BACKGROUND = WHITE

MIRROR_NONE = 0x00
MIRROR_HORIZONTAL = 0x01
MIRROR_VERTICAL = 0x02
MIRROR_ORIGIN = 0x03

ROTATE_0 = 0
ROTATE_90 = 90
ROTATE_180 = 180
ROTATE_270 = 270

AROUND = 1  # dot pixel 1x1
RIGHTUP = 2  # dot pixel 2X2
DOT_STYLE_DFT = AROUND


class EPD_GUI():
    def __init__(self):
        self.epd = EPD_2Inch7()
        self.epd.reset()
        self.epd.hw_init()      
        self.img_portrait = bytearray(EPD_HEIGHT * EPD_WIDTH//8)
        self.img_landscape = bytearray(EPD_HEIGHT * EPD_WIDTH//8)
        self.draw_portrait = framebuf.FrameBuffer(self.img_portrait, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)
        self.draw_landscape = framebuf.FrameBuffer(self.img_landscape, EPD_HEIGHT, EPD_WIDTH, framebuf.MONO_VLSB)
        self.mem_w = EPD_WIDTH
        self.mem_h = EPD_HEIGHT
        self.color = WHITE
        self.rotate = ROTATE_270
        self.mirror = MIRROR_VERTICAL
        if EPD_WIDTH % 8 == 0:
            self.byte_w = EPD_WIDTH//8
        else:
            self.byte_w = (EPD_WIDTH // 8) + 1
        self.byte_h = EPD_HEIGHT
        if self.rotate == ROTATE_0 or self.rotate == ROTATE_180:
            self.w = EPD_WIDTH
            self.h = EPD_HEIGHT
        else:
            self.w = EPD_HEIGHT
            self.h = EPD_WIDTH
#         print("mem_w:",self.mem_w,"mem_h:",self.mem_h,"byte_w:",self.byte_w,"byte_h:",self.byte_h)
