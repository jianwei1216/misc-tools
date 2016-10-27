#!/usr/bin/python
#coding:UTF-8

import os
import sys
import datetime
import psutil as ps

def get_all_process_pids():
    all_pids = ps.pids()
    print all_pids

def get_one_process_info():
    print '===================系统所有进程pid==================='
    print 'system pids:', ps.pids()
    print '===================进程具体信息======================'
    p = ps.Process(29042)
    print 'process name:', p.name()
    print 'process pid:', p.pid
    print 'process ppid:', p.ppid()
    print 'process parent:', p.parent()
    print 'process bin:', p.exe()
    print 'process cwd:', p.cwd()
    print 'process uername:', p.username()
    print 'process status:', p.status()
    print 'process create time:', datetime.datetime.fromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')
    print 'process uid:', p.uids()
    print 'process gid:', p.gids()
    print 'process cpu times:', p.cpu_times()
    print 'process memory percent:', p.memory_percent()
    print 'process memory info:', p.memory_info()
    print 'process io-count:', p.io_counters()
    print 'process num threads:', p.num_threads()
    print 'process connections:', p.connections()
    print '===================系统内存=========================='
    print 'system virtual memory:', ps.virtual_memory()
    print '===================系统交换空间======================'
    print 'system swap memory:', ps.swap_memory()
    print '===================系统分区=========================='
    print 'system disk partitions:', ps.disk_partitions()
    print '===================某个分区的使用情况================'
    print 'system disk usage:', ps.disk_usage('/')
    print '===================系统总I/O========================='
    print 'system disk io counters:', ps.disk_io_counters()
    print '===================系统各分区I/O====================='
    print 'system disk io counters:', ps.disk_io_counters(perdisk=True)
    print '===================系统网络总I/O====================='
    print 'system net io counters:', ps.net_io_counters()
    print '===================系统各网卡I/O====================='
    print 'system net io counters:', ps.net_io_counters(pernic=True)

if __name__ == '__main__':
    #get_all_process_pids()
    get_one_process_info()
