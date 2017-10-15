"""
Want to test roland's brain to see if he get's bored!

"""

from rolandbrain import RolandBrain


if __name__=="__main__":
    brain = RolandBrain()

    objects = ['cat', 'dog', 'cheese', 'cat', 'mince', 'cheese']

    for i in objects:
        brain.update(i)

        print "bored = ", brain.bored
