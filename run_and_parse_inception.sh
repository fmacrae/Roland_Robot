#! /bin/bash

( cd /home/pi/tensorflow && ./label_image --image=../Roland_Robot/$1) &> ../Roland_Robot/raw.output  
tail -5 raw.output | cut -d"]" -f2 | cut -d"(" -f1 > $2
