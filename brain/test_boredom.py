"""
Want to test roland's brain to see if he get's bored!

"""

from rolandbrain import RolandBrain
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__=="__main__":
    brain = RolandBrain()

    objects = ['cat', 'dog', 'cheese', 'lollipop', 'prison', 'laundry', 'basket', 'castle', 'god', 'art', 'beans']

    # get some observations based on the objects above
    # observations = {}

    boredom = []

    for i in range(1000):
        seen = objects[np.random.randint(0,10)]
        brain.update(seen)

        print "bored = ", brain.bored
        boredom.append(brain.bored)


    info_gains = pd.Series(brain.information_gains)
    plt.figure()
    ax = info_gains[0:300].plot(color='blue', linewidth=2)
    plt.xlabel('Observations')
    plt.ylabel(r'Information gain ($\Delta S$)')
    plt.tight_layout()
    plt.savefig('information_gain.png')

