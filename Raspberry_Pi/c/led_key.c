#include <stdio.h>
#include "led_key.h"
#include "sg_lgpio.h"
#include <unistd.h>
#include <stdint.h>


//define pin conection in BCM number
/****************************
* PIN_D1     4 
* PIN_D2     18 
* PIN_K1     27
* PIN_K2     22
***************************/

void LED_KEY_Init(void)
{
    //Lgpio_export(); 
    Lgpio_set_pinmode(PIN_D1,LGPIO_OUTPUT);
    Lgpio_set_pinmode(PIN_D2,LGPIO_OUTPUT);
    Lgpio_set_pinmode(PIN_K1,LGPIO_INPUT);
    Lgpio_set_pinmode(PIN_K2,LGPIO_INPUT);
}

void Led_key_task(void)
{
	int k1_flag = 0;
	int k2_flag = 0;	
	printf("Led Key Task\r\n");
	for(;;)
	{
	    //K1 key
	    if(Lgpio_read_pin(PIN_K1) == LGPIO_LOW && k1_flag == 0)
	    {
	        delay(10);
			if(Lgpio_read_pin(PIN_K1) == LGPIO_LOW) // make sure the button has been pressed
			{
				k1_flag = 1;
				Lgpio_write_pin(PIN_D1,LGPIO_HIGH);
				printf("K1 Press\r\n");
			}
	    }
	    else if(Lgpio_read_pin(PIN_K1) == LGPIO_HIGH && k1_flag == 1) // key has been released
	    {
			k1_flag = 0;
			Lgpio_write_pin(PIN_D1,LGPIO_LOW);
	    } 
	    //K2 key
	    if(Lgpio_read_pin(PIN_K2) == LGPIO_LOW && k2_flag == 0)
	    {
	        delay(10);
			if(Lgpio_read_pin(PIN_K2) == LGPIO_LOW) // make sure the button has been pressed
			{
				k2_flag = 1;
				Lgpio_write_pin(PIN_D2,LGPIO_HIGH);
				printf("K2 Press\r\n");
			}
	    }
	    else if(Lgpio_read_pin(PIN_K2) == LGPIO_HIGH && k2_flag == 1) // key has been released
	    {
			k2_flag = 0;
			Lgpio_write_pin(PIN_D2,LGPIO_LOW);
	    } 
	}
}


/***********************************************************
						end file
***********************************************************/

