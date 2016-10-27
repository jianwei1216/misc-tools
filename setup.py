#!/usr/bin/python

import os
import sys

SRC_BIN_PATH = './bin/'
SRC_LIB_PATH = './lib/'
DST_BIN_PATH = '/usr/local/bin/'
DST_LIB_PATH = '/usr/local/my-scripts/lib/' 

def init_config_file (file_path):
    try:
        if not file_path:
            print ('Arg is invalid(file_path=%s)' % (file_path))
            return False

        if not os.path.isdir (file_path):
            os.makedirs (file_path)

        return True
    except Exception, e:
        print "%s" % (e)
        return False

def install():
    try:
        if not init_config_file (DST_BIN_PATH):
            print ("Failed to init BIN_PATH!")
            return -1

        if not init_config_file (DST_LIB_PATH):
            print ("Failed to init LIB_PATH!")
            return -1

        bin_copy_cmd = '\cp -f ' + SRC_BIN_PATH + '* ' + DST_BIN_PATH
        lib_copy_cmd = '\cp -f ' + SRC_LIB_PATH + '* ' + DST_LIB_PATH
        print 'DEBUG', bin_copy_cmd
        os.system (bin_copy_cmd)
        print 'DEBUG', lib_copy_cmd
        os.system (lib_copy_cmd)

        return 0
    except Exception, e:
        print "%s" % (e)
        return -1

def clean ():
    try:
        if not init_config_file (DST_BIN_PATH):
            print ("Failed to init BIN_PATH!")
            return -1

        if not init_config_file (DST_LIB_PATH):
            print ("Failed to init LIB_PATH!")
            return -1

        bin_rm_cmd = 'rm -f ' + DST_BIN_PATH + 'multi_threads_write_read_test.py '
        lib_rm_cmd = 'rm -rf ' + DST_LIB_PATH + '* '
        print 'DEBUG', bin_rm_cmd
        os.system (bin_rm_cmd)
        print 'DEBUG', lib_rm_cmd
        os.system (lib_rm_cmd)

        return 0
    except Exception, e:
        print "%s" % (e)
        return -1

if __name__ == '__main__':
    if len (sys.argv) != 2:
        print 'Usage: %s [install|clean]' % (sys.argv[0])
        exit (0)

    op = sys.argv[1]
    if op == 'install':
        install ()
    elif op == 'clean':
        clean ()
    else:
        print 'Usage: %s [install|clean]' % (sys.argv[0])
        exit (0)

