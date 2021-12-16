import gym, gym.spaces, gym.utils, gym.utils.seeding
import numpy as np
from battleship import Board 
from battleship.static_board_v1 import ship_config 

BOARD_DIM = 10 


class BattleshipEnvClass(gym.Env):
    """ BattleshipEnvClass 

        action_space is a index representing grid coordinate to probe next 
        obs_space is the entire (n x n) grid with discrete values (-1, 0, 1) 

    """
    def __init__(self):
        
        self.board_dim = BOARD_DIM  

        # Action space is index of action for grid.flatten() 
        #   get i, j with i, j = (action % BOARD_DIM, action // BOARD_DIM)
        self.action_space = gym.spaces.Discrete(BOARD_DIM * BOARD_DIM)

        # Observation space is an integer array that summarizes knowledge of each  
        #    grid block according to:   {0: unknown, 1: hit, -1: miss}
        self.observation_space = gym.spaces.Box(low=-1, high=1, 
            shape=(BOARD_DIM, BOARD_DIM), dtype=np.int32)        
        
        self.reset()
    

    def step(self, action):

        state_prev = np.copy(self.state) 
        action_coord = (action % BOARD_DIM, action // BOARD_DIM)

        ####################
        # ADVANCE ENVIRONMENT -- Produce next state, check done condition   
        hit = self.board.torpedo(action_coord) 
        
        if hit == 0: 
            self.state[action_coord[0], action_coord[1]] = -1 
        elif hit == 1: 
            self.state[action_coord[0], action_coord[1]] =  1 
        else: 
            raise ValueError("Invalid return from board.torpedo(), f{hit}")

        self.done = self.board.check_gameover()


        ####################
        # REWARD CALCULATION  
        #   Write your reward mechanism here 

        reward = -1 

        if hit:
            reward += 2    



        info = {}
        return self.state, reward, self.done, info
    
    def render(self):
        """ Emtpy.  The Board renders itself upon action given vis=True  
        """
        pass
    
    def reset(self):

        self.board = Board(dim=self.board_dim, ship_config='default', vis=False, playmode=False)

        # Uncomment this for a frozen board state between training iterations 
#         self.board = Board(dim=self.board_dim, ship_config=ship_config, vis=False, playmode=False)

        self.state = np.zeros((self.board_dim, self.board_dim), dtype=np.int32) 
        self.done = False 

        return self.state
        
    
    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]


    def _overwrite_board(self, board): 
        self.board = board 