#!/usr/bin/python
#conding:UTF-8

import random
import os
import sys
import time

def test_down_up ():
    while True:
        os.system ('ifconfig enp1s0f0 down')      
        sleep_time = random.randint (5, 30)
        time.sleep (sleep_time)
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        os.system ('ifconfig enp1s0f0 up')      
        sleep_time = random.randint (300, 600)
        time.sleep (sleep_time)

if __name__ == '__main__':
    test_down_up ()

