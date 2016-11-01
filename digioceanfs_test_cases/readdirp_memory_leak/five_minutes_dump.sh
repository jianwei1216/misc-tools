#!/usr/bin/bash

for (( i=0; i<6; i++ )); do
    kill -USR1 4324
    sleep 300
done

