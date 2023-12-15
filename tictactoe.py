import numpy as np

class TicTacToe():
    def __init__(self):
        self.board = np.array([[0, 0, 0], # 0 blank, 1 1p, 2 2p
                               [0, 0, 0],
                               [0, 0, 0]])
        self.game_over = False
 
    def get_possible_actions(self) -> np.array: # Unit Test complete
        available_actions = np.where(self.board == 0) # [[yyy...],[xxx...]]  format
        action_idxs = np.column_stack((available_actions[0], available_actions[1])) # [[y, x], [y, x], ...] format
        return action_idxs
        
    def update_game_status(self): # Unit Test complete
        # Check for win condition
        for player in [1, 2]:
            if np.any(np.all(self.board == player, axis=0)) \
               or np.any(np.all(self.board == player, axis=1)) \
               or np.all(np.diag(self.board) == player) \
               or np.all(np.diag(np.fliplr(self.board)) == player):
                self.game_over = True
                return 2 # Return 1 for a win

        # Check for draw
        if not np.any(self.board == 0):
            self.game_over = True
            return 0 # Return 0 for a draw

        return 0 # Return 0 for ongoing game
    
    def reset(self):
        self.board = np.array([[0, 0, 0], 
                               [0, 0, 0],
                               [0, 0, 0]])                          
        self.game_over = False