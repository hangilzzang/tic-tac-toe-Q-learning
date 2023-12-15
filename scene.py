import pygame
import sys, os
class Scene:
    def __init__(self, screen):
        
        # to make exe file
        # if getattr(sys, 'frozen', False):
        #     application_path = sys._MEIPASS
        # else:
        #     application_path = os.path.dirname(os.path.abspath(__file__))

        # self.play_file_path = os.path.join(application_path, 'data', 'play.npy')
        # self.replay_file_path = os.path.join(application_path, 'data', 'replay.npy')    
        
        
        
        self.next_scene = None
        
        size = screen.get_size()  # get screen size
        self.width, self.height = size
            
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.bg_color = (28, 170, 156)
        self.line_color = (23, 145, 135)
        self.button_color =  (253, 253, 150)
        self.white = (255, 255, 255)
        self.soft_red = (255, 128, 128)

    def handle_events(self, events):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError

    def draw_text(self, screen, text, position, color, size):
        font = pygame.font.SysFont('segoeui', size)
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(center=position)
        screen.blit(rendered_text, text_rect)