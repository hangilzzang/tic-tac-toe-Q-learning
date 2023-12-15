import pygame
from scene import Scene
import numpy as np
from q_learning import QLearning
from tictactoe import TicTacToe

class ReplayScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.game = TicTacToe()
        self.agent = QLearning(self.game)
        
        self.replay = np.load('replay.npy')
        # self.replay = np.load(self.replay_file_path) # to make exe file
        
        self.board_size = min(self.width, self.height)
        self.line_width = int(self.board_size * 1/30) # you can decide the thickness of tic-tac-toe line here
        self.board_size_rate = 0.6 # you can dicide the board size of tic-tac-toe here 0~1
        self.board_size = int(self.board_size * self.board_size_rate)
        
        self.x1 = int((self.width - self.board_size) * 1/2)
        self.y1 = int((self.height - self.board_size) * 1/2)
   
        self.board1 = int(self.board_size * 1/3)
        self.board2 = int(self.board_size * 2/3)
        
        self.line = pygame.Rect(self.x1 + self.line_width * 1/2, self.y1 + self.line_width * 1/2, self.board_size - self.line_width, self.board_size - self.line_width)
        self.tictactoe_tiles = self.make_tictectoe_tile() # make click event detecting tictactoe tile   
        
        self.previous = pygame.Rect(self.width * 1/9, self.height * 2/5, self.width * 1/9, self.height * 1/9)
        self.pre_clicked = False
        self.next = pygame.Rect(self.width * 7/9, self.height * 2/5, self.width * 1/9, self.height * 1/9)
        self.next_clicked =False
        self.menu = pygame.Rect(self.width * 9/12, self.height * 8/10, self.width * 1/6, self.height * 1/12)
        self.menu_clicked = False
        
        self.input_box = pygame.Rect(self.width * 3/10 , self.height * 8/10, self.width * 1/5, self.height * 1/10)
        
        self.font = pygame.font.SysFont('segoeui', 32)
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.black)
        
        self.searched = False
        self.episode_num = 0
        self.num = None
        self.epi_idx = -1
        self.agent.p1 = True
        self.episode = self.replay[self.episode_num]
        self.next_move()
        
        
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
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # if user clicked
                
                if self.input_box.collidepoint(event.pos):
                        self.active = True

                else:
                    self.active = False
                   
                    if self.next.collidepoint(event.pos):
                        self.next_clicked = True
                    
                    if self.previous.collidepoint(event.pos):
                        self.pre_clicked = True
                    
                        
                    elif self.menu.collidepoint(event.pos):
                        self.menu_clicked = True
                        
                
                
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN: 
                        self.searched = True
                        self.num = self.text  
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]  
                    else:
                        self.text += event.unicode  
                    
                    self.txt_surface = self.font.render(self.text, True, self.black)
    
    def next_move(self):
        self.episode = self.replay[self.episode_num]
        if self.epi_idx < 8 and self.epi_idx >= -1:
            action = self.episode[self.epi_idx + 1]
            if not np.array_equal(action, np.array([-1, -1])):
                self.agent.p1 = False if self.epi_idx % 2 == 0 else True
                self.agent.take_action(action) 
                self.epi_idx = self.epi_idx + 1
 
                
    def previous_move(self):
        self.episode = self.replay[self.episode_num]
        if self.epi_idx <= 8 and self.epi_idx >=0:
            action = self.episode[self.epi_idx]
            if not np.array_equal(action, np.array([-1, -1])):
                self.game.board[tuple(action)] = 0
                self.epi_idx = self.epi_idx - 1
                
    def update(self):
        if self.searched:
            self.searched = False
            if type(self.num) != int:
                if self.num.isdigit():   
                    self.num = int(self.num)
                else:
                    return
            if self.num >= 0 and len(self.replay)>self.num:
                self.episode_num = self.num
                self.epi_idx = -1
                self.game.reset()
                self.next_move()
    
        
        elif self.next_clicked:
            self.next_move()
            self.next_clicked = False
    
        elif self.pre_clicked:
            self.previous_move()
            self.pre_clicked = False
            
        elif self.menu_clicked:
            self.next_scene = 'main_menu_scene'
           
    
    def render(self, screen):
        screen.fill(self.bg_color)
        pygame.draw.rect(screen, self.line_color, self.line)
        for i in self.tictactoe_tiles:
            pygame.draw.rect(screen, self.bg_color, i)  

        
        pygame.draw.rect(screen, self.soft_red, self.previous)  
        pygame.draw.rect(screen, self.soft_red, self.next)  
        pygame.draw.rect(screen, self.button_color, self.menu)  
        pygame.draw.rect(screen, self.white, self.input_box)

        self.draw_text(screen, 'main menu', self.menu.center, self.black, 20)
        self.draw_text(screen, 'next', self.next.center, self.black, 20)
        self.draw_text(screen, 'previous', self.previous.center, self.black, 20)
        self.draw_text(screen, f'/{len(self.replay)-1} ', (self.width * 5/8, self.height * 17/20), self.black, 40)

        text_colors = {'O': self.red, 'X': self.black}
        for i in range(9):
            sym = ['','X','O'][self.game.board[(i % 3, i // 3)]] 
            if sym in ['O', 'X']:
                self.draw_text(screen, sym, self.tictactoe_tiles[i].center, text_colors[sym], 100)
        
        screen.blit(self.txt_surface, (self.input_box.x+5, self.input_box.y+5))