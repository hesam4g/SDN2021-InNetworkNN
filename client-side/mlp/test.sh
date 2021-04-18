#!/bin/bash

for i in $( eval echo {1..$1} )
do
   python3 sender.py &
   sleep 1
done
