#!/usr/bin/python

import os
import logging
import logging.config

#log_conf = "./log.conf"
log_conf = "/usr/local/my-scripts/lib/log.conf"

try:
    os.mkdir('/var/log/my-scripts')
    os.system('touch /var/log/my-scripts/fast.log')
    os.system('touch /var/log/my-scripts/misc.log')
    os.system('touch /var/log/my-scripts/cluster.log')
    os.system('touch /var/log/my-scripts/ixgbe_network_test.log')
    os.system('touch /var/log/my-scripts/multi_threads_write_read.log')
except:
    pass

logging.config.fileConfig(log_conf)
fastlog = logging.getLogger('fastCommandLoger')
misclog = logging.getLogger('miscLoger')
clusterlog = logging.getLogger('clusterLoger')
netlog = logging.getLogger('networkLoger')
mtwrlog = logging.getLogger ('mtwrLoger')

def test():
    fastlog.info('This is info message')
    fastlog.debug('This is DEBUG message')
    fastlog.warn('This is Warning message')
    fastlog.error('This is Error message')
    fastlog.critical('This is critical message')

    misclog.info('This is info message')
    misclog.debug('This is DEBUG message')
    misclog.warn('This is Warning message')
    misclog.error('This is Error message')
    misclog.critical('This is critical message')

    clusterlog.info('This is info message')
    clusterlog.debug('This is DEBUG message')
    clusterlog.warn('This is Warning message')
    clusterlog.error('This is Error message')
    clusterlog.critical('This is critical message')

    netlog.info('This is info message')
    netlog.debug('This is DEBUG message')
    netlog.warn('This is Warning message')
    netlog.error('This is Error message')
    netlog.critical('This is critical message')

    mtwrlog.info('This is info message')
    mtwrlog.debug('This is DEBUG message')
    mtwrlog.warn('This is Warning message')
    mtwrlog.error('This is Error message')
    mtwrlog.critical('This is critical message')

if __name__ == "__main__":
    test()
