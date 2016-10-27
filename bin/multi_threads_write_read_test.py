#!/usr/bin/python
#-*- coding:UTF-8 -*-

import sys
import os
import thread
import argparse
import uuid

sys.path.append ('/usr/local/my-scripts/lib/')
from log import mtwrlog

'''
1.对同一个文件，一写一读;
2.对同一个文件, 一写多读;
3.对同一个文件，一读多写；
'''

MAX_RANDOM_INT = 10000000000

def get_random_file_name (dir=False):
    try:
        uuid_str = str (uuid.uuid1())
        file_name = ''
        for i in uuid_str.split('-'):
            if file_name == '':
                file_name += i
            else:
                file_name += '_' + i

        if dir:
            file_name += '_' + 'dir'
        else:
            file_name += '_' + 'file'

        return file_name
    except Exception, e:
        mtwrlog.critical ("Failed to run get_random_file_name(): %s" % (e))
        return -1

def one_write_one_read_test ():
    pass

def one_write_multi_read_test ():
    pass

def one_read_multi_write_test (work_dir, dir_depth, dir_count, file_count):
    try:
          
    except Exception, e:
        mtwrlog.critical ('Failed to run one_read_multi_write_test(): %s' % (e))
        return -1

if __name__ == '__main__':
    get_random_file_name()
    exit(0)
    try:
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
        parser.add_argument ('--run-hour-time', type=int,
                             help='脚本运行时长，若未指定，则跑到指定')
        args = parser.parse_args ()

        if args.one_write_one_read:
            pass
        elif args.one_write_multi_read:
            pass
        elif args.one_read_multi_write:
            pass
        else:
            parser.print_usage ()
    except Exception, e:
        print "%s" % (e)
        mtwrlog.critical ("%s" % e)
        exit (-1)
