import pygame

from src.utils import *
from src.game import Game
from src.title_screen import titleScreen



class Window:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Madżong")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_mode = "title"
        init_assets()
        self.current_screen : Screen = titleScreen(self.screen)
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
                        self.__click_handler(self.current_screen.release_left())
                        
                        
                                
            self.current_screen.draw(self.pos)
            pygame.display.flip()
            self.clock.tick(FPS)
            
    def __click_handler(self, click_index: int | None) -> None:
        if click_index is not None:
            self.game_mode = CLICK_STATES[self.game_mode][click_index]
            match self.game_mode:
                case "title":
                    self.current_screen = titleScreen(self.screen)
                case "game":
                    self.current_screen = Game(self.screen)