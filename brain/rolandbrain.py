"""
Andy McMahon: Roland the lego-hooverbot, ML club.
"""
directions = 3 # forward, left 90, right 90

import qlearn
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RolandBrain(object):

    def __init__(self):
        self.ai = None
        self.ai = qlearn.QLearn(actions=range(directions),
                                alpha=0.1, gamma=0.9, epsilon=0.1)

        # 1 or 0 depending on whether roland is bored.
        self.bored = 0
        self.num_times_bored_recently = 0 # will put a time limit / number of moves limit on this
        self.bored_to_death = 0
        self.lastState = None
        self.lastAction = None
        self.objects_seen = []
        self.num_total_observations = 0

    def go_in_direction(self, direction):

        #=============
        # send command to controller to move in direction, map {'0': forward, '1': left', '2:'right'}
        #=============
        logger.info('Move direction: %s', direction)
        logger.info('Number observations: %s', self.num_total_observations)
        logger.info('Number objects seen: %s', self.objects_seen)
        return None

    def update(self, new_object):
        self.num_total_observations += 1
        state = self.calcState(new_object)
        reward = -1

        if state == 'bored':
            reward = -10
        elif state == 'not_bored':
            reward = 50
        if self.lastState is not None:
            self.ai.learn(self.lastState, self.lastAction, reward, state)

        action = self.ai.chooseAction(state)
        self.lastState = state
        self.lastAction = action

        self.go_in_direction(action)

    def calcState(self, new_object):

        if new_object in self.objects_seen:
            self.bored = 1
            self.num_times_bored_recently += 1
            return 'bored'
        elif new_object not in self.objects_seen:
            self.bored = 0
            self.objects_seen.append(new_object)
            return 'not_bored'


