"""
Andy McMahon: Roland the lego-hooverbot, ML club.
"""
directions = 4 # forward, left 90, right 90

import AIclasses.qlearn as qlearn
import logging
import math
import os


class RolandBrain(object):

    def __init__(self, logPath=None):
        # If we implement a qlearn method.
        self.ai = qlearn.QLearn(actions=range(directions),
                                alpha=0.1, gamma=0.9, epsilon=0.1)

        # 1 or 0 depending on whether roland is bored.
        self.bored = 0
        self.num_times_bored_recently = 0 # will put a time limit / number of moves limit on this
        self.bored_to_death = 0
        self.lastState = None
        self.lastAction = None
        self.observations = {} # keys = object, values = number of times
        self.num_total_observations = 0
        self.observational_entropy = 0
        self.information_gains = []

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        if logPath is None:
            hdlr = logging.FileHandler('brain.log')
        else:
            hdlr = logging.FileHandler(os.path.join(logPath, 'brain.log'))

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)

        self.logger = logger

    def calculate_observational_entropy(self):

        total_obs = sum(self.observations.values())
        probs = [1.0*i/total_obs for i in self.observations.values()]

        entropy = sum(map(lambda x: -x*math.log(x), probs))

        return entropy

    def go_in_direction(self, direction):

        #=============
        # send command to controller to move in direction, map {'0': forward, '1': left', '2:'right'}
        #=============
        self.logger.info('suggestedMove: %s', direction)
        self.logger.info('obsNumber: %s', self.num_total_observations)
        self.logger.info('observations: %s', str(self.observations))
        self.logger.info('obsEntropy: %s', str(self.observational_entropy))
        return None

    def update(self, new_object):
        # have seen something!
        self.num_total_observations += 1

        # Have I seen this before, am I bored?
        state = self.calcState(new_object)

        # get a small -ve reward irrespective of anything.
        reward = -1

        # how do I feel?
        if state == 'bored':
            reward = -10

        elif state == 'not_bored':
            reward = 50
        # If I have a q-dictionary to refer to, use it
        if self.lastState is not None:
            self.ai.learn(self.lastState, self.lastAction, reward, state)

        # choose an action based on my state and comparison with past above if performed
        action = self.ai.chooseAction(state)

        # update my variables
        self.lastState = state
        self.lastAction = action

        # let's move somewhere that hopefully lessens my boredom.
        self.go_in_direction(action)

    def calcState(self, new_object):
        boredom = 'not_bored'

        # If I've seen this object before
        if new_object in self.observations.keys():
            # I'm bored
            self.bored = 1
            self.num_times_bored_recently += 1
            # record the fact I've seen this object again
            self.observations[new_object] += 1
            boredom =  'bored'

        # if this object is new to me
        elif new_object not in self.observations.keys():
            # I'm not bored
            self.bored = 0
            self.observations[new_object] = 1
            boredom = 'not_bored'

        # calculate and record my information gain
        current_entropy = self.observational_entropy
        new_entropy = self.calculate_observational_entropy()
        self.observational_entropy = new_entropy

        information_gain = new_entropy - current_entropy

        self.information_gains.append(information_gain)
        return boredom



