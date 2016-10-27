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
            os.system ('ifconfig eno2 down')      
            sleep_time = 60
            time.sleep (sleep_time)
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            os.system ('ifconfig eno2 up')      
            time.sleep (1)
            os.system ('ifconfig eno2 up')      
            sleep_time = 3600
            time.sleep (sleep_time)
    else:
        return 0

if __name__ == '__main__':
    test_down_up ()

