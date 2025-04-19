import pygame

from src.utils import *
from src.tile_matrix import tileMatrix
from src.tile import Tile



class Game(Screen):
    
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.matrix = tileMatrix(self.screen, (BOARD_WIDTH, BOARD_DEPTH, BOARD_HEIGHT))
        
        self.matrix.generate_board(MODEL2)
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.blit(TILES_TEXTURES["bg"], (0, 0))
        self.selected_tile: Tile | None = None
        self.pressed_tile: Tile | None = None
        self.hovered_tile: Tile | None = None
        self.hovered_coords: tuple[int, int, int] | None = None
        self._buttons.append(Button(self.screen, 20, 20, 60, 60, "", TILES_TEXTURES["arrow_left"]))
        
    def draw(self, pos) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.hovered_tile, self.hovered_coords = self.matrix.draw(pos)
        super().draw(pos)
        
    def press_left(self) -> None:
        self.pressed_tile = self.hovered_tile
        super().press_left()
    
    def release_left(self) -> None:
        if (self.pressed_tile == self.hovered_tile and self.hovered_tile is not None and
            self.matrix.can_be_removed(self.hovered_coords)):
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
        return super().release_left()
        
    
        