"""
ROLAND'S BRAIN MOFO!
"""

from brain.rolandbrain import RolandBrain
import numpy as np

# will get this from current run txt

with open("data/current_run.txt", "r") as f:
    lineList = f.readlines()

logPath = 'data/' + lineList[-1].rstrip()


if __name__ == "__main__":

    brain = RolandBrain(logPath=logPath)


    objects = ['cat', 'dog', 'cheese', 'lollipop', 'prison', 'laundry', 'basket', 'castle', 'god', 'art', 'beans']

    for i in range(1000):
        seen = objects[np.random.randint(0,10)]
        brain.update(seen)


