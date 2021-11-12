import gym, gym.spaces, gym.utils, gym.utils.seeding
import numpy as np


class SimpleEnv(gym.Env):
    
    def __init__(self):
        self.action_space = gym.spaces.box.Box(low=0,high=1, shape=(2,), dtype=np.float32)
        self.observation_space = gym.spaces.box.Box(low=0,high=10, shape=(4,), dtype=np.float32)
        self.reset()
    
    def step(self, action):
        self.state = np.array([action[0],action[0],action[1],action[1]], dtype=np.float32)
        reward = 1
        done = False
        
        info = {}
        return self.state, reward, done, info
    
    def render(self):
        pass
    
    def reset(self):
        self.state = np.array([0,0,0,0], dtype=np.float32)
        return self.state
        
    
    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]