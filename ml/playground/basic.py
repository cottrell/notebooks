import gym
import numpy as np
import gym.spaces
from gym import error, spaces, utils
from gym.utils import seeding

class BasicEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, n_instr=100):
        self.state = None
        self.observation_space = None # really? This is a pain ... why do we need to specify this
        self.action_space = gym.spaces.Box(low=np.zeros(n_instr), high=np.ones(n_instr), dtype=np.float32)

    def _step(self, action):
        """
        Returns
        -------
        ob, reward, episode_over, info : tuple
        """
        self._take_action(action)
        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = self.status != hfo_py.IN_GAME
        return ob, reward, episode_over, {}

    def _reset(self):
        pass

    def _render(self, mode='human', close=False):
        pass

    def _take_action(self, action):
        pass

    def _get_reward(self):
        """ Reward is given for XY. """
        if self.status == FOOBAR:
            return 1
        elif self.status == ABC:
            return self.somestate ** 2
        else:
            return 0

b = BasicEnv()
