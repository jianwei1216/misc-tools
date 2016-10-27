#!/usr/bin/python
#conding:UTF-8

import random
import os
import sys
import time

def test_down_up ():
    pid = os.fork()
    if pid == 0:
        while True:
            sleep_time = random.randint (10, 30)
            os.system ('ifconfig eno2 down')      
            time.sleep (sleep_time)
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            sleep_time = random.randint (600, 900)
            os.system ('ifconfig eno2 up')      
            time.sleep (1)
            os.system ('ifconfig eno2 up')      
            time.sleep (sleep_time)
    else:
        return 0

if __name__ == '__main__':
    test_down_up ()

