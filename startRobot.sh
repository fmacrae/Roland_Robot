#! /bin/bash
sh setMaxVol.sh
python Panning.py &
python autonomous.py &
python recursive_image.py --image_file='/dev/shm/mjpeg/cam.jpg' --warmup_runs=1 --num_runs=40 &
