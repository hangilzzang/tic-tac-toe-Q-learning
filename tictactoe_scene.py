import pygame
from scene import Scene
import numpy as np
from q_learning import QLearning
from tictactoe import TicTacToe

class TicTacToeScene(Scene):
    def __init__(self, screen):
        self.scene_stage = 0
        super().__init__(screen)
        self.O = pygame.Rect(self.width * 1/7, self.height * 1/4, self.width * 2/7, self.height * 2/7)
        self.X = pygame.Rect(self.width * 4/7, self.height * 1/4, self.width * 2/7, self.height * 2/7)
        self.back_to_menu = pygame.Rect(self.width * 4/12, self.height * 9/12, self.width * 2/6, self.height * 1/12)
        
        self.click_obj = {'O' : {'obj': self.O, 'clicked': False},
                          'X' : {'obj': self.X, 'clicked': False},
                          'menu': {'obj': self.back_to_menu, 'clicked': False}}
        

        self.game = TicTacToe()
        self.agent = QLearning(self.game)
        
        self.agent.q_table = np.load('play.npy')
        # self.agent.q_table = np.load(self.play_file_path) # to make exe file
        
        
        self.board_size = min(self.width, self.height)
        self.line_width = int(self.board_size * 1/30) # you can decide the thickness of tic-tac-toe line here
        self.board_size_rate = 0.8 # you can dicide the board size of tic-tac-toe here 0~1
        self.board_size = int(self.board_size * self.board_size_rate)
        
        self.x1 = int((self.width - self.board_size) * 1/2)
        self.y1 = int((self.height - self.board_size) * 1/2)
   
        self.board1 = int(self.board_size * 1/3)
        self.board2 = int(self.board_size * 2/3)
        
        self.line = pygame.Rect(self.x1 + self.line_width * 1/2, self.y1 + self.line_width * 1/2, self.board_size - self.line_width, self.board_size - self.line_width)
        self.tictactoe_tiles = self.make_tictectoe_tile() # make click event detecting tictactoe tile   

        self.players_turn = True # if true player takes first turn
        self.agent.p1 = True
        self.action_idxs = None
        self.player_action = None
        self.r = None

        
    def make_tictectoe_tile(self): 
        tictactoe_tiles = []
        for i in [self.x1 + self.line_width * 1/2, 
                  self.x1 + self.board1 + self.line_width * 1/2,
                  self.x1 + self.board2 + self.line_width * 1/2]:
            for j in [self.y1 + self.line_width * 1/2, 
                      self.y1 + self.board1 + self.line_width * 1/2, 
                      self.y1 + self.board2 + self.line_width * 1/2]:
                tictactoe_tile=pygame.Rect(i, j, self.board1 - self.line_width, self.board1 - self.line_width)             
                tictactoe_tiles.append(tictactoe_tile)
        return tictactoe_tiles
    
    

    
    def handle_events(self, events):
        if self.scene_stage == 0:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for _, value in self.click_obj.items():
                        if value['obj'].collidepoint(event.pos):
                            value['clicked'] = True
        

        elif self.game.game_over == False:
            if self.action_idxs is None:
                self.action_idxs = self.game.get_possible_actions() 

            elif self.players_turn:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for tile_idx in range(len(self.tictactoe_tiles)):
                            if self.tictactoe_tiles[tile_idx].collidepoint(event.pos):
                                self.player_action = np.array([tile_idx % 3, tile_idx // 3]) # change format
                                self.tile_idx = tile_idx
                                if not np.any(np.all(self.player_action == self.action_idxs, axis=1)): # if players action not valid
                                    self.player_action = None


        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for _, value in self.click_obj.items():
                        if value['obj'].collidepoint(event.pos):
                            value['clicked'] = True
                               
    
    def update_game(self):
        self.r = self.game.update_game_status() 
        if self.game.game_over == False:
            self.action_idxs = None
            self.player_action = None
            self.players_turn = not self.players_turn
            self.agent.p1 = not self.agent.p1
        
    
                     
                
    def update(self):
        if self.scene_stage == 0:
            if self.click_obj['O']['clicked'] == True:
                self.players_turn == False
                self.scene_stage += 1
            elif self.click_obj['X']['clicked'] == True:
                self.players_turn == True
                self.scene_stage += 1


        elif self.game.game_over == False: # if game is ongoing
            if self.players_turn:
                if self.player_action is not None:
                    self.agent.take_action(self.player_action) # Player Action!
                    self.update_game()            
            else:
                _, greedy_action, _ = self.agent.calculate_actions(self.action_idxs)
                self.agent.take_action(greedy_action[-2:])
                self.update_game()
        
        elif self.scene_stage == 1:
            self.scene_stage += 1
            pygame.time.delay(1500)
            self.text = f'{['O','X'][self.agent.p1]} WIN!' if self.r != 0 else 'DRAW!' 
            
        else:
            if self.click_obj['menu']['clicked'] == True:
                self.next_scene = 'main_menu_scene'

            
    def render(self, screen):
        
        if self.scene_stage == 0:
            screen.fill(self.bg_color)
            pygame.draw.rect(screen, self.button_color, self.O)  
            self.draw_text(screen, 'O', self.O.center, self.black, 40)          
            pygame.draw.rect(screen, self.button_color, self.X)  
            self.draw_text(screen, 'X', self.X.center, self.black, 40)    
            self.draw_text(screen, 'choose your character', (int(self.width * 1/2), int(self.height * 3/4)), self.black, 50)
        
        
        elif self.scene_stage == 1:
            screen.fill(self.bg_color)
            pygame.draw.rect(screen, self.line_color, self.line)
            for i in self.tictactoe_tiles:
                pygame.draw.rect(screen, self.bg_color, i)  
            
            text_colors = {'O': self.red, 'X': self.black}
            for i in range(9):
                sym = ['','X','O'][self.game.board[(i % 3, i // 3)]] 
                if sym in ['O', 'X']:
                    self.draw_text(screen, sym, self.tictactoe_tiles[i].center, text_colors[sym], 100)
 
        else:
            screen.fill(self.bg_color) 
            pygame.draw.rect(screen, self.button_color, self.back_to_menu)  
            self.draw_text(screen, self.text, (int(self.width * 1/2), int(self.height * 1/2)), self.black, 100)
            self.draw_text(screen, 'main menu', self.back_to_menu.center, self.black, 20)