#ifndef __LED_KEY_H
#define __LED_KEY_H

#include "sys.h"

//IO settings
#define D1_Pin   5 
#define D2_Pin   6 
#define K1_Pin   7 
#define K2_Pin   8 

#define D1_on   PBout(5)=1 
#define D1_off  PBout(5)=0

#define D2_on   PBout(6)=1
#define D2_off  PBout(6)=0

#define K1_value      PBin(7)
#define K2_value      PBin(8)

////////FUNCTION//////
void Led_key_task(void);

#endif
