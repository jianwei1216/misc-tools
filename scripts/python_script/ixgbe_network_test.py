#!/usr/bin/python
#-*- coding:UTF-8 -*-

# 测试问题：http://10.10.1.12/mantis/view.php?id=8153
# 本脚本测试结果正确的现象应为/var/log/my-scripts/ixgbe_network_test.log中
# 对应的ip(pid)不存在连接失败的日志信息。
# 本脚本测试方法:
# 每睡眠300s则尝试连接test_node，若连接成功则reboot, 失败则打印错误日志

import socket
import argparse
import sys
import os
import ssh
import time
import traceback
import fcntl
from log import netlog

command_lock_file = '/var/run/ixgbe_network_test.pid'

def command_log (argv):
    try:
        if not argv or len(argv) == 0:
            netlog.error ('args are invalid!(args=%s)' % (argv))
            return -1

        command_line = 'python'
        for arg in argv:
            command_line += ' ' + arg

        netlog.debug (command_line)
    except Exception, e:
        netlog.critical ('Failed to run command_log(): %s' % (e))
        return -1


def init_config_file (file_path, logger=netlog):
    try:
        if not file_path:
            logger.error ('Arg is invalid(file_path=%s)' % (file_path))
            return False

        config_file_dir = os.path.dirname (file_path)
        if not os.path.isdir (config_file_dir):
            os.makedirs (config_file_dir)

        os.mknod (file_path)
        return True
    except Exception, e:
        logger.error ('Failed init_config_file(file_path=%s): ' \
                        '%s (traceback=%s)' % (file_path, e, \
                        traceback.format_exc().split('\n')))
        return False

def command_lock (command_lock_file, logger=netlog):
    try:
        global command_lock_fd
        global command_locked
        command_locked = False

        if not os.path.isfile (command_lock_file):
            init_config_file (command_lock_file)

        command_lock_fd = open (command_lock_file, 'ab')
        if fcntl.flock (command_lock_fd, fcntl.LOCK_EX) == -1:
            logger.error ('Failed to get command lock ' \
                            '(command_lock_file=%s)' % (command_lock_file))
            return False

        command_lock_fd.truncate(0)
        command_lock_fd.write(str(os.getpid()))
        command_lock_fd.flush()
        command_locked = True
        return True
    except Exception, e:
        logger.error ('Failed to get command lock for ' \
                        'pid_file(%s): %s (traceback=%s)' % (command_lock_file,\
                        e, traceback.format_exc().split('\n')))
        return False

def command_unlock (command_lock_file, logger=netlog):
    try:
        global command_lock_fd
        global command_locked

        if not os.path.isfile (command_lock_file):
            init_config_file (command_lock_file)

        if not command_locked:
            return True

        if fcntl.flock (command_lock_fd, fcntl.LOCK_UN) == -1:
            logger.error ('Failed to command unlock ' \
                            '(pid_file=%s)' % (command_lock_file))
            return False

        command_locked = False
        command_lock_fd.truncate(0)
        command_lock_fd.close()
        return True
    except Exception, e:
        logger.error ('Failed to command unlock for pid_file(%s): ' \
                        '%s (traceback=%s)' % (command_lock_file, e, \
                        traceback.format_exc().split('\n')))
        return False

def get_ssh_client(host, port, username, password, logger=netlog):
    try:
        global args
        if not host or not port or not username or not password:
            logger.error ('Args are invalid!')
            return -1

        client = ssh.SSHClient()
        client.set_missing_host_key_policy(ssh.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password)

        return client
    except Exception, e:
        logger.critical ("%s: %s" % (host, e))
        return -1

def __client_exec_commands (host, port, username, password,
                            cmd_list, sleep=0, logger=netlog):
    try:
        if not host or not port or not username or not password \
                or len(cmd_list) == 0:
            logger.error ('Args are invalid! (host=%s, port=%s, username=%s,'
                          'password=%s, cmd_list=%s)' % (host, port, username,
                          password, cmd_list))
            return -1

        client = get_ssh_client(host, port, username, password, cmd_list)
        if client == -1:
            logger.error ('Failed to get client_handle')
            return -1

        for cmd in cmd_list:
            logger.info ("%s, %s" % (host, cmd))
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read()
            err = stderr.read()
            if len(err) > 0:
                logger.error ("%s: %s" % (host, err))
            if len(out) > 0:
                logger.info ("%s: %s" % (host, out))
            if sleep != 0:
                time.sleep(sleep)

        client.close()
        return 0
    except Exception, e:
        logger.critical ('Failed to run __client_exec_commands(): %s' % (e))
        return -1
        
def test_network (nodes, port, username, password):
    try:
        if not nodes or len(nodes) == 0 or \
                not port or len(password) == 0 or not username:
            netlog.error ('Arg is invalid!(nodes=%s, port=%s, '
                          'username=%s, password=%s)' \
                          % (nodes, port, username, password))
            return -1
        
        for node in nodes:
            pid = os.fork ()
            if pid == 0:
                while True:
                    locked = False
                    try:
                        sk = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
                        sk.connect ((node, port))
                        command_lock (command_lock_file)
                        locked = True
                        netlog.info ('Success to connect (node=%s, port=%s)'
                                     'pid=%s' % (node, port, os.getpid()))

                        cmd_list = []
                        reboot_cmd = 'reboot'
                        cmd_list.append (reboot_cmd)
                        ret = __client_exec_commands (node, port, username,
                                                      password, cmd_list)
                        if ret < 0:
                            exit(ret)
                        if locked:
                            command_unlock (command_lock_file)
                            locked = False
                        time.sleep (300)
                        continue
                    except Exception, e:
                        if locked:
                            command_unlock (command_lock_file)
                            locked = False
                        netlog.error ('Failed to connect (node=%s, port=%s): '
                                      '%s (pid=%s)' % (node, port, e,
                                      os.getpid()))
                        continue
            else:
                print '--debug--', node
        return 0
    except Exception, e:
        netlog.critical ('Failed to run test_network(): %s' % (e))
        return -1

if __name__ == '__main__':
    try:
        global args

        command_log (sys.argv)
        parser = argparse.ArgumentParser ()
        parser.add_argument ('--test-start', action='store_true',
                             help='start the test') 
        parser.add_argument ('--test-stop', action='store_true',
                             help='stop the test') 
        parser.add_argument ('--test-nodes', nargs='+', help='test nodes ip')
        parser.add_argument ('-p', '--port', nargs='?', default=9999,
                             help='connect port(default=9999)')
        parser.add_argument ('--password', type=str, help='ssh password')
        parser.add_argument ('--username', type=str, help='ssh username')
        args = parser.parse_args ()

        if args.test_start:
            test_network (args.test_nodes, int(args.port), args.username,
                          args.password)
        elif args.test_stop:
            pass
        else:
            parser.print_usage ()
            exit(0)
    except Exception, e:
        print e
        exit (-1)
