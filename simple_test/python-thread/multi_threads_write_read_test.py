#!/usr/bin/python
#-*- coding:UTF-8 -*-

import sys
import os
import thread
import argparse

'''
1.对同一个文件，一写一读;
2.对同一个文件, 一写多读;
3.对同一个文件，一读多写；
'''

def get_random_file_name ():
    pass

def one_write_one_read_test ():
    pass

def one_write_multi_read_test ():
    pass

def one_read_multi_write_test ():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser ()
    parser.add_argument ('--one-write-one-read', action='store_true',
                         help='一写一读')
    parser.add_argument ('--one-write-multi-read', action='store_true',
                         help='一写多读')
    parser.add_argument ('--one-read-multi-write', action='store_true',
                         help='一读多写')
    parser.add_argument ('--work-dir', type=str,
                         help='工作目录')
    parser.add_argument ('--dir-depth', type=int, default='0',
                         help='目录深度(默认值=0)')
    parser.add_argument ('--dir-count', type=int,
                         help='目录数量')
    parser.add_argument ('--file-count', type=int,
                         help='文件数量')
    args = parser.parse_args ()

    if args.one_write_one_read:
        pass
    elif args.one_write_multi_read:
        pass
    elif args.one_read_multi_write:
        pass
    else:
        parser.print_usage ()
