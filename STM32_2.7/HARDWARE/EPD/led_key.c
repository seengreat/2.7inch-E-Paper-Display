#include <string.h>
#include <stdlib.h>    
#include "delay.h"
#include "led_key.h"
#include "usart.h"


/////////////////EPD settings Functions/////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////
void Led_key_task(void)
{
	int k1_flag = 0;
	int k2_flag = 0;	
	printf("Led Key Task\r\n");
	for(;;)
	{
	    //K1 key
	    if(K1_value == 0 && k1_flag == 0)
	    {
	        delay_ms(10);
			    if(K1_value == 0) // make sure the button has been pressed
			    {
				     k1_flag = 1;
				     D1_on;
				     printf("K1 Press\r\n");
			    }
	    }
	    else if(K1_value == 1 && k1_flag == 1) // key has been released
	    {
			    k1_flag = 0;
			    D1_off;
	    }  
	    //K2 key
	    if(K2_value == 0 && k2_flag == 0)
	    {
	        delay_ms(10);
			    if(K2_value == 0) //make sure the button has been pressed
			    {
				     k2_flag = 1;
				     D2_on;
				     printf("K2 Press\r\n");
			    }
	    }
	    else if(K2_value == 1 && k2_flag == 1) // key has been released
	    {
			    k2_flag = 0;
			    D2_off;
	    } 
  }
}


//////////////////////////////////END//////////////////////////////////////////////////
