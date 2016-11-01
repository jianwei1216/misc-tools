#!/usr/bin/bash

#cd /cluster2/test/
#
#for i in {10001..100000}; do
#    echo touch newfile$i
#    touch newfile$i
#done
#
#cd /
#
count=0
while [[ 1 ]]; do
    #echo ls /cluster2/test/ && sleep 10
    #ls /cluster2/test/ && sleep 10
    echo df -h /cluster2/test/
    df -h /cluster2/test/ && sleep 1
done
