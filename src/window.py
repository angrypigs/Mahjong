import pygame

from src.utils import *
from src.game import Game



class Window:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Madżong")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_mode = 1
        init_assets()
        self.current_screen : Screen = Game(self.screen)
        self.pos = (0, 0)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.current_screen.press_left()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.current_screen.release_left()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_screen.matrix.generate_board(MODEL2)
                        
                        
                                
            self.current_screen.draw(self.pos)
            pygame.display.flip()
            self.clock.tick(FPS)
            