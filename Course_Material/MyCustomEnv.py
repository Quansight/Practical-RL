import gym, gym.spaces, gym.utils, gym.utils.seeding
import numpy as np


class MyCustomEnvClass(gym.Env):
    
    def __init__(self):
        self.action_space = gym.spaces.box.Box(
            low=np.array([-40.0, -40.0], dtype=np.float32),
            high=np.array([40.0, 40.0], dtype=np.float32))
        self.observation_space = gym.spaces.box.Box(
            low=np.array([-100, -100, -100, -100, 0], dtype=np.float32),
            high=np.array([100, 100, 100, 100, 360], dtype=np.float32))
        #alternative way of writing the obs space if all high/low are the same: gym.spaces.box.Box(low=-100,high=100, shape=(4,), dtype=np.float32)
        self.init_x = 30
        self.init_y = 30
        self.heading = 0
        self.timestep = 0.5
        self.reset()
    
    def step(self, action):
        self.heading += action[0]
        self.heading = self.heading%360
        throttle = action[1]/40
        angle_to_move = self.heading * np.pi / 180.0
        
        old_distance = np.linalg.norm([self.target_x - self.x, self.target_y - self.y])
        
        self.x += throttle*self.timestep*np.cos(angle_to_move)
        self.y += throttle*self.timestep*np.sin(angle_to_move)
        
        new_distance = np.linalg.norm([self.target_x - self.x, self.target_y - self.y])
        
        reward = float(old_distance - new_distance)
        self.state = np.array([self.target_x, self.target_y, self.x, self.y, self.heading], dtype=np.float32)
        done = self.done
        
        info = {}
        return self.state, reward, done, info
    
    def render(self):
        pass
    
    def reset(self):
        self.target_x = self.init_x
        self.target_y = self.init_y
        self.x = 0
        self.y = 0
        self.done = False
        self.state = np.array([self.target_x, self.target_y, self.x, self.y, self.heading], dtype=np.float32)
        return self.state
        
    
    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]