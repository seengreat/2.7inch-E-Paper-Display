#ifndef __LED_KEY_H
#define __LED_KEY_H

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "Arduino.h"

//IO settings
#define D1_Pin   4 
#define D2_Pin   5 
#define K1_Pin   16 
#define K2_Pin   17 

#define D1_on  digitalWrite(D1_Pin,HIGH) 
#define D1_off  digitalWrite(D1_Pin,LOW)

#define D2_on  digitalWrite(D2_Pin,HIGH) 
#define D2_off  digitalWrite(D2_Pin,LOW)

#define K1_value       digitalRead(K1_Pin)
#define K2_value       digitalRead(K2_Pin)

////////FUNCTION//////
void Led_key_task(void);

#endif
