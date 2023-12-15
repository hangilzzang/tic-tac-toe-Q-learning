import random
import numpy as np

class QLearning():
    def __init__(self, game, initial_alpha = 1, alpha_decay = 0.99999, minimum_alpha = 0.01, delta = 0.9, initial_epsilon = 1, epsilon_decay = 0.99999, epsilon_min = 0.1):
        self.q_table = np.zeros((3,3,3,3,3,3,3,3,3,3,3))

        self.initial_alpha = initial_alpha
        self.alpha_decay = alpha_decay
        self.minimum_alpha = minimum_alpha
        self.alpha = self.initial_alpha
        self.delta = delta
        self.initial_epsilon = initial_epsilon 
        self.epsilon_decay = epsilon_decay
        self.minimum_epsilon = epsilon_min
        self.epsilon = initial_epsilon


        self.game = game
        self.history = [[None, None, None],[None, None, None]] # [[p2_qsa, p2_r, p2_maxq_val], [p1_qsa, p1_r, p1_maxq_val]]
        self.p1 = True
        
    def calculate_actions(self, action_idxs) -> (np.array, np.array, np.float64): # Unit Test complete
        state_idx = self.game.board.flatten() 
        q_idxs = np.array([np.concatenate((state_idx, action_idx)) for action_idx in action_idxs]) # [[state_idx + yx], [state_idx + yx]] format
        random_action = random.choice(q_idxs) # get random action
        q_values = np.array([self.q_table[tuple(q_idx)] for q_idx in q_idxs]) # q_idxs into q_value
        max_q_index = np.argmax(q_values)
        max_q_value = q_values[max_q_index] # get max q value
        greedy_action = q_idxs[max_q_index] # get greedy action
                       
        return random_action, greedy_action, max_q_value
    
    def update_table(self): # Unit Test complete
        if self.history[self.p1][0] is not None and self.history[self.p1][1] is not None and self.history[self.p1][2] is not None:        
            self.q_table[tuple(self.history[self.p1][0])] = self.q_table[tuple(self.history[self.p1][0])] + (self.alpha * (self.history[self.p1][1] + (self.delta * self.history[self.p1][2]) - self.q_table[tuple(self.history[self.p1][0])])) # normal update
        elif self.history[self.p1][0] is not None and self.history[self.p1][1] is not None:
            self.q_table[tuple(self.history[self.p1][0])] = self.q_table[tuple(self.history[self.p1][0])] + (self.alpha * (self.history[self.p1][1] - self.q_table[tuple(self.history[self.p1][0])])) # game over update
        else:
            pass
              
    def select_action(self, random_action, greedy_action): # Unit Test complete
        coin = random.random()
        if coin < self.epsilon: # exploration
            return random_action
        else: # exploitation
            return greedy_action
        

    def take_action(self, action):
        stone = 1 if self.p1 else 2   
        self.game.board[tuple(action)] = stone # action!