import json

import pygame

from src.utils import *
from src.game import Game
from src.title_screen import titleScreen
from src.level_editor import levelEditor
from src.level_choice import levelChoice
from src.tile_matrix import tileMatrix

from tests.generate_board_test import generate_board_test



class Window:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Madżong")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_mode = "title"
        init_assets()
        self.__load_levels()
        # generate_board_test("ac201c6b-7e72-44f0-865c-07ac92bebfca")
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
            
    def __load_levels(self) -> None:
        matrix = tileMatrix(self.screen, (BOARD_WIDTH, BOARD_DEPTH, BOARD_HEIGHT))
        for level in os.listdir(ROAMING_PATH / "levels"):
            try:
                p = ROAMING_PATH / "levels" / level
                with p.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    name = data["name"]
                    uuid = data["uuid"]
                    model = [[[bool(int(z)) for z in list(y)] for y in x.split(".")] for x in data["matrix"].split(",")]
                    miniature = pygame.transform.smoothscale(matrix.create_miniature(model, name), 
                        (WIDTH // 4, HEIGHT // 4))
                    LEVELS[uuid] = [model, miniature, name]
            except Exception as e:
                print(f"Error at level {level}: {e}")
        
            
    def __click_handler(self, click_index: str | None) -> None:
        print(click_index)
        if click_index is not None:
            self.game_mode = click_index
            match self.game_mode:
                case "title":
                    self.current_screen = titleScreen(self.screen)
                case "editor":
                    self.current_screen = levelEditor(self.screen)
                case "choice":
                    self.current_screen = levelChoice(self.screen)                  
                case _:
                    if self.game_mode.startswith("level:"):
                        name = self.game_mode[6:]
                        self.current_screen = Game(self.screen, name, LEVELS[name][0])
                            