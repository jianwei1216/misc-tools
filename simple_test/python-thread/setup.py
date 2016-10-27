#!/usr/bin/python

import os
import sys
import shutil

BIN_PATH = '/usr/local/bin/'
LIB_PATH = '/usr/local/my-scripts/'

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
        if not init_config_file (BIN_PATH):
            print ("Failed to init BIN_PATH!")
            return -1

        if not init_config_file (LIB_PATH):
            print ("Failed to init LIB_PATH!")
            return -1
        
    except Exception, e:
        print "%s" % (e)
        return -1
      

def clean ():
    pass

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

