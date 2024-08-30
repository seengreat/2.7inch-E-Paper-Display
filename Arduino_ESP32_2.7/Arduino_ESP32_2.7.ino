#include "epd_demo.h"
#include "epd_2inch7.h"
#include "epd_gui.h"
#include "led_key.h"
#include "fonts.h"
#include <SPI.h>
/***************************************************************************************
 * Project  :
 * Experimental Platform :Arduino ESP32 + 2.7inch E-Paper Display
 * Hardware Connection :Arduino ESP32-> 2.7inch E-Paper
 *      IO27 --> CS
 *      IO18 --> CLK
 *      IO23 --> MOSI
 *      IO14  --> DC
 *      IO33  --> RST
 *      IO13  --> BUSY
 * Author      : Andy Li
 * Web Site    :www.seengreat.com
***************************************************************************************/
/******************************
 * image :
 * 0------------> x (1~264) 
 * |
 * |
 * |
 * |
 * y (1~176)
 * 
 * */
void setup() {

   pinMode(BUSY_Pin, INPUT_PULLUP); 
   pinMode(RES_Pin, OUTPUT);
   EPD_W21_RST_1;  
   pinMode(DC_Pin, OUTPUT);    
   pinMode(CS_Pin, OUTPUT);    
   pinMode(SCK_Pin, OUTPUT);    
   pinMode(SDI_Pin, OUTPUT);

   pinMode(D1_Pin, OUTPUT);    
   pinMode(D2_Pin, OUTPUT);
   pinMode(K1_Pin, INPUT_PULLUP); 
   pinMode(K2_Pin, INPUT_PULLUP); 
   
}

unsigned char image[5808];//Define canvas space  

//Tips//
/*
1.When the e-paper is refreshed in full screen, the picture flicker is a normal phenomenon, and the main function is to clear the display afterimage in the previous picture.
2.When the partial refresh is performed, the screen does not flash.
3.After the e-paper is refreshed, you need to put it into sleep mode, please do not delete the sleep command.
4.Please do not take out the electronic paper when power is on.
5.Wake up from sleep, need to re-initialize the e-paper.
6.When you need to transplant the driver, you only need to change the corresponding IO. The BUSY pin is the input mode and the others are the output mode.
*/
void loop() {
    unsigned char i,Miao_L,Miao_H,Fen_L,Fen_H; 

    EPD_HW_Init(); //Electronic paper initialization
    EPD_WhiteScreen_White();
    EPD_WhiteScreen_ALL(gImage_0); //Refresh the picture in full screen need 2.72s
    delay(2000);
    //Clear
    EPD_HW_Init(); //EPD init
    EPD_WhiteScreen_White();//EPD Clear
    EPD_WhiteScreen_ALL_Fast(gImage_1);//EPD_picture1   
    EPD_DeepSleep();//EPD_DeepSleep,Sleep instruction is necessary, please do not delete!!!
    delay(2000);     
//    //////////////////////Partial refresh time demo/////////////////////////////////////
    EPD_HW_Init(); //Electronic paper initialization  
    EPD_SetRAMValue_BaseMap(gImage_basemap); //Partial refresh background color 2.1s  
    Miao_H = 0;
    Fen_L = 0;
    Fen_H = 0;        
    for(Miao_L=0;Miao_L<10;Miao_L++)
    {
         //EPD_Dis_Part_myself function                    
         EPD_Dis_Part_myself(64,77,Num[Miao_L],  //x-A,y-A,DATA-A
                64,109,Num[Miao_H],         //x-B,y-B,DATA-B
                64,149,gImage_numdot,      //x-C,y-C,DATA-C
                64,191,Num[Fen_L],         //x-D,y-D,DATA-D
                64,223,Num[Fen_H],32,64);  //x-E,y-E,DATA-E,Resolution 32*64 
         delay(100);    
    }
////////////////////////////////////////////////////////////////////////  
  //Clear screen
    EPD_HW_Init(); //Electronic paper initialization
    EPD_WhiteScreen_White(); //Show all white
    EPD_DeepSleep();  //Enter deep sleep,Sleep instruction is necessary, please do not delete!!!
    delay(2000);    
    ///////////////////////////GUI///////////////////////////////////////////////////////////////////////////////////
   //Data initialization settings
    Image_Init(image, EPD_WIDTH, EPD_HEIGHT, 90, WHITE); //Set screen size and display orientation

    /**************Drawing**********************/
    EPD_HW_Init_GUI(); //EPD init GUI
    Gui_Clear(WHITE);
    //Point   
    Gui_Draw_Point(3, 1, BLACK, PIXEL_1X1, DOT_STYLE_DFT);
    Gui_Draw_Point(3, 15, BLACK, PIXEL_2X2, DOT_STYLE_DFT);
    Gui_Draw_Point(5, 40, BLACK, PIXEL_4X4, DOT_STYLE_DFT);
    Gui_Draw_Point(5, 55, BLACK, PIXEL_8X8, DOT_STYLE_DFT);
    //Line
    Gui_Draw_Line(5, 5,30, 110, BLACK, PIXEL_1X1, SOLID);
    Gui_Draw_Line(5, 30, 45, 30, BLACK, PIXEL_1X1, SOLID);
    //Rectangle
    Gui_Draw_Rectangle(20, 5, 95, 80, BLACK, EMPTY, PIXEL_1X1);
    Gui_Draw_Rectangle(70, 45, 115, 95, BLACK, FULL, PIXEL_1X1);
    //Circle
    Gui_Draw_Circle(200, 60, 30, BLACK, EMPTY, PIXEL_1X1);
    Gui_Draw_Circle(226, 75, 18, BLACK, FULL, PIXEL_1X1);
    Gui_Draw_Str(20, 102, "abcdefg", &Font12, WHITE, BLACK); //7*12
    Gui_Draw_Str(100, 100, "ABCabc012345", &Font16, WHITE, BLACK); //11*16
    Gui_Draw_Str(40, 120, "2.7\" E-Paper", &Font20, WHITE, BLACK); //14*20
    Gui_Draw_Str(47, 145, "SEENGREAT", &Font24, WHITE, BLACK); //17*24

    EPD_Display(image);//display image need 2.74s
    EPD_DeepSleep();//EPD_DeepSleep,Sleep instruction is necessary, please do not delete!!!
    delay(3000);         
  
    //Clear screen
    EPD_HW_Init(); //Electronic paper initialization
    EPD_WhiteScreen_White(); //Show all white
    EPD_DeepSleep();  //Enter deep sleep,Sleep instruction is necessary, please do not delete!!!
    delay(2000);  
    Led_key_task();
    while(1); 
}
