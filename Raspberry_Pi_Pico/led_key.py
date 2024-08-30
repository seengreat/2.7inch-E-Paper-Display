from utime import *
from machine import Pin,

PIN_D1     = 21
PIN_D2     = 20
PIN_K1     = 18
PIN_K2     = 17

if __name__ == '__main__':
    D1 = Pin(PIN_D1, Pin.OUT)
    D2 = Pin(PIN_D2, Pin.OUT)
    D1.value(0)
    D2.value(0)
    K1 = Pin(PIN_K1, Pin.IN, Pin.PULL_UP)
    K2 = Pin(PIN_K2, Pin.IN, Pin.PULL_UP)
    k1_flag = 0
    k2_flag = 0
    while True:
        if K1.value() == 0 and k1_flag == 0:
            sleep_ms(10)
            if K1.value() == 0: # make sure the button has been pressed
                k1_flag = 1
                D1.value(1)
                print("K1 Press")
        elif K1.value() == 1 and k1_flag == 1: # key has been released
            k1_flag = 0
            D1.value(0)
            
        if K2.value() == 0 and k2_flag == 0:
            sleep_ms(10)
            if K2.value() == 0: # make sure the button has been pressed
                k2_flag = 1
                D2.value(1)
                print("K2 Press")
        elif K2.value() == 1 and k2_flag == 1: # key has been released
            k2_flag = 0
            D2.value(0)
            
            
            
            
            