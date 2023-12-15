import numpy as np
from q_learning import QLearning
from tictactoe import TicTacToe
from tqdm import tqdm

def learn():
    game = TicTacToe()
    agent = QLearning(game) # you can decide epsilon and alpha rate here
    # initial_alpha = 1, alpha_decay = 0.99999, minimum_alpha = 0.01, delta = 0.9, initial_epsilon = 1, epsilon_decay = 0.99999, epsilon_min = 0.1
    
    whole_learning_history = []
    for _ in tqdm(range(200000)): # episode num
        learning_history = []
        agent.p1 = True # p1 always takes first turn
        while True:
            action_idxs = game.get_possible_actions()
            random_action, greedy_action, max_q_value = agent.calculate_actions(action_idxs) # get maxq_val
            agent.history[agent.p1][2] = max_q_value
            agent.update_table() # update q table
            action = agent.select_action(random_action, greedy_action) # get qsa
            agent.take_action(action[-2:]) # ACTION! and update board
            learning_history.append(action[-2:])
            agent.history[agent.p1][0] = action
            r = game.update_game_status() # get r                           
            agent.history[agent.p1][1] = r 
            agent.history[agent.p1][2] = None
            if game.game_over:
                agent.update_table()
                agent.p1 = not agent.p1
                agent.history[agent.p1][1] = r  if r == 0 else -1              
                agent.update_table()
                break 
            else:
                agent.p1 = not agent.p1
        
        whole_learning_history.append(learning_history)
        agent.alpha = agent.alpha * agent.alpha_decay # alpha decrease 
        agent.epsilon = agent.epsilon * agent.epsilon_decay # epsilon decrease 
        game.reset()
    
    print(agent.alpha)
    print(agent.epsilon)
    # padding before save history
    max_length = max([len(episode) for episode in whole_learning_history]) # find longest episode length
    padded_episodes = []
    for episode in whole_learning_history:
        padded_episode = episode + ([np.array([-1, -1])] * (max_length - len(episode)))
        padded_episodes.append(padded_episode)      
    np_episodes = np.array(padded_episodes)

    np.save('replay.npy', np_episodes) # save learning history
    np.save('play.npy', agent.q_table) # save Q_table 



learn()