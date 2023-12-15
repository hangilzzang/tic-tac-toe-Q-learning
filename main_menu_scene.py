import pygame
from scene import Scene

class MainMenuScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)  
        self.ai_button = pygame.Rect(self.width * 1/3, self.height * 4/9, self.width * 1/3, self.height * 1/9)  
        self.play_clicked = False
        self.replay_button = pygame.Rect(self.width * 1/3, self.height * 7/9, self.width * 1/3, self.height * 1/9)  
        self.replay_clicked = False
            



    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.ai_button.collidepoint(event.pos):
                    self.play_clicked = True
                elif self.replay_button.collidepoint(event.pos):
                    self.replay_clicked = True

    def update(self):
        if self.play_clicked:
            self.next_scene = 'tictactoe_scene'
        elif self.replay_clicked:
            self.next_scene = 'replay_scene'

    def render(self, screen):
        screen.fill(self.bg_color)

        pygame.draw.rect(screen, self.button_color, self.ai_button)  
        pygame.draw.rect(screen, self.button_color, self.replay_button)  
        
        self.draw_text(screen, 'Play with AI', self.ai_button.center, self.black, 36)
        self.draw_text(screen, 'Replay', self.replay_button.center, self.black, 36)
        self.draw_text(screen, 'RL TIC-TAC-TOE!', (self.width * 1/2, self.height * 1/6), self.black, 45)
        
