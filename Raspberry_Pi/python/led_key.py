import time
from gpiozero import *

'''define pin conection in BCM number
2.7inch_EPD    Raspberry Pi
      D1   --->   D4
      D2   --->   D18
      K1   --->   D27
      K2   --->   D22
'''
PIN_D1     = 4
PIN_D2     = 18
PIN_K1     = 27
PIN_K2     = 22

if __name__ == '__main__':
    D1 = DigitalOutputDevice( PIN_D1,active_high = True,initial_value =False)#
    D2 = DigitalOutputDevice( PIN_D2,active_high = True,initial_value =False)#    
    K1 = DigitalInputDevice(PIN_K1,pull_up=True,active_state=None)
    K2 = DigitalInputDevice(PIN_K2,pull_up=True,active_state=None)
    k1_flag = 0
    k2_flag = 0
    while True:
        if K1.value == 1 and k1_flag == 0:
            time.sleep(0.01)
            if K1.value == 1: # make sure the button has been pressed
                k1_flag = 1
                D1.on()
                print("K1 Press")
        elif K1.value == 0 and k1_flag == 1: # key has been released
            k1_flag = 0
            D1.off()
            
        if K2.value == 1 and k2_flag == 0:
            time.sleep(0.01)
            if K2.value == 1: # make sure the button has been pressed
                k2_flag = 1
                D2.on()
                print("K2 Press")
        elif K2.value == 0 and k2_flag == 1: # key has been released
            k2_flag = 0
            D2.off()
            
            
            
            
            