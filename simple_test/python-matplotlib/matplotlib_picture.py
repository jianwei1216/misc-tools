#!/usr/bin/python
#coding:UTF-8

import numpy as np
import matplotlib
matplotlib.use ('Agg')
from matplotlib.pyplot import plot, savefig

def test1():
    x = np.linspace (-4, 4, 30)
    y = np.sin (x)

    plot (x, y, '--*b')

    savefig ('MyFig.jpg')

def zhe_xian_tu():
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]
    plot (x, y)
    y.reverse()
    print x
    print y
    plot (x, y)
    savefig ('zhe_xian_tu.jpg')

if __name__ == '__main__':
    #test1 ()
    zhe_xian_tu ()
