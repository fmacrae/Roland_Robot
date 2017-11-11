"""
ROLAND'S BRAIN MOFO!
"""

from brain.rolandbrain import RolandBrain
import numpy as np
import os

# will get this from current run txt

with open("run_data_directory.txt", "r") as f:
    lineList = f.readlines()

#logPath = 'data/' + lineList[-1].rstrip()
logPath = lineList[-1].rstrip()

if not os.path.exists(logPath):
    os.makedirs(logPath)

if __name__ == "__main__":

    brain = RolandBrain(logPath=logPath)


    objects = ['cat', 'dog', 'cheese', 'lollipop', 'prison', 'laundry', 'basket', 'castle', 'god', 'art', 'beans']

    for i in range(1000):
        seen = objects[np.random.randint(0,10)]
        brain.update(seen)


