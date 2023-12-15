import pygame
from main_menu_scene import MainMenuScene
from tictactoe_scene import TicTacToeScene
from replay_scene import ReplayScene




def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600)) # you can change display size
    pygame.display.set_caption("Tic Tac Toe Game")

    scenes = {
        'main_menu_scene': MainMenuScene,
        'tictactoe_scene': TicTacToeScene,
            'replay_scene': ReplayScene
    }

    current_scene = MainMenuScene(screen)
    
    while current_scene is not None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                current_scene = None
                break    
            current_scene.handle_events(events)
            current_scene.update()
            current_scene.render(screen)
            if current_scene.next_scene:
                scene_class = scenes.get(current_scene.next_scene)
                current_scene = scene_class(screen)
        pygame.display.update()

    pygame.quit()

run_game()