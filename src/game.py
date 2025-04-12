import pygame

from src.utils import *
from src.tile_matrix import tileMatrix
from src.tile import Tile



class Game(Screen):
    
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.matrix = tileMatrix(self.screen, (BOARD_WIDTH, BOARD_DEPTH, BOARD_HEIGHT))
        board = [[[bool(i % 2 == 0 and j % 2 == 0 and i < 12 and j < 12) for i in range(BOARD_WIDTH * 2 - 1)]
                  for j in range(BOARD_DEPTH * 2 - 1)]
                 for k in range(BOARD_HEIGHT)]
        self.matrix.generate_board(board)
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.blit(TILES_TEXTURES["bg"], (0, 0))
        self.selected_tile: Tile | None = None
        self.pressed_tile: Tile | None = None
        self.hovered_tile: Tile | None = None
        
    def draw(self, pos) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.hovered_tile = self.matrix.draw(pos)
        
    def press_left(self) -> None:
        self.pressed_tile = self.hovered_tile
    
    def release_left(self) -> None:
        if self.pressed_tile == self.hovered_tile and self.hovered_tile is not None:
            if self.selected_tile is None:
                self.pressed_tile.selected = True
                self.selected_tile = self.pressed_tile
            else:
                if self.selected_tile.type == self.pressed_tile.type and self.selected_tile != self.pressed_tile:
                    self.matrix.remove_tiles([self.selected_tile, self.pressed_tile])
                else:
                    self.selected_tile.selected = False
                self.selected_tile = None
        self.pressed_tile = None
        self.hovered_tile = None
        
    
        