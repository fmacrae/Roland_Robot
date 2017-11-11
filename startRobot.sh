#! /bin/bash
sh setMaxVol.sh
python recursive_image.py --image_file='/dev/shm/mjpeg/cam.jpg' --warmup_runs=1 --num_runs=40 &
python Panning.py &
python autonomous.py &

