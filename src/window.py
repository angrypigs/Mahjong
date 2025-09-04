import json

import pygame

from src.utils import *
from src.game import Game
from src.title_screen import titleScreen
from src.level_editor import levelEditor



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
            
    def __click_handler(self, click_index: str | None) -> None:
        print(click_index)
        if click_index is not None:
            self.game_mode = click_index
            match self.game_mode:
                case "title":
                    self.current_screen = titleScreen(self.screen)
                case "editor":
                    self.current_screen = levelEditor(self.screen)
                case _:
                    if self.game_mode.startswith("level:"):
                        level_path = ROAMING_PATH / "levels" / f"{self.game_mode[6:]}.json"
                        with level_path.open('r', encoding='utf-8') as f:
                            data = json.load(f)
                            name = data["name"]
                            model = [[[bool(int(z)) for z in list(y)] for y in x.split(".")] for x in data["matrix"].split(",")]
                            self.current_screen = Game(self.screen, name, model)