"""
Want to test roland's brain to see if he get's bored!

"""

from rolandbrain import RolandBrain
import numpy as np

if __name__=="__main__":
    brain = RolandBrain()

    objects = ['cat', 'dog', 'cheese', 'lollipop', 'prison', 'laundry', 'basket', 'castle', 'god', 'art', 'beans']

    # get some observations based on the objects above
    #observations = {}
    boredom = []
    for i in range(1000):
        seen = objects[np.random.randint(0,10)]
        brain.update(seen)

        print "bored = ", brain.bored
        boredom.append(brain.bored)
    #    if seen in observations.keys():
    #        observations[seen] += 1
    #    else:
    #        observations[seen] = 1

    # run through the observations and see how Roland's brain does.
    #for i in observations:
    #    brain.update(i)

    #    print "bored = ", brain.bored
