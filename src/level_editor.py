import pygame

from src.utils import *
from src.tile_matrix import tileMatrix
from src.tile import Tile



class levelEditor(Screen):
    
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.blit(TILES_TEXTURES["bg"], (0, 0))
        self.matrix = tileMatrix(self.screen, (BOARD_WIDTH, BOARD_DEPTH, BOARD_HEIGHT))
        for h in range(self.matrix.size[2]):
            for d in range(self.matrix.size[1]):
                for w in range(self.matrix.size[0]):
                    self.matrix.place_tile(h, d, w, special="editor_point", info=f"{h} {d} {w}", counts=False)
        self.current_layer = 0
        self.pressed_tile: Tile | None = None
        self.hovered_tile: Tile | None = None
        self.hovered_coords: tuple[int, int, int] | None = None
        
    def draw(self, pos) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.hovered_tile, self.hovered_coords = self.matrix.draw(pos, layers=[self.current_layer])
        super().draw(pos)
        
    def press_left(self):
        self.pressed_tile = self.hovered_tile
        super().press_left()
        
    def release_left(self):
        if (self.pressed_tile == self.hovered_tile and self.hovered_tile is not None):
            h, d, w = self.hovered_coords
            if self.matrix.can_be_placed(self.hovered_coords):
                self.matrix.matrix[h][d][w].type = "Blank"
                self.matrix.matrix[h][d][w].counts = True
                self.matrix.matrix[h][d][w].special = ""
                for row in range(-1, 2):
                    for col in range(-1, 2):
                        if in_bounds(h, d + col, w + row, 
                                  self.matrix.size[2], 
                                  self.matrix.size[1], 
                                  self.matrix.size[0]) and (row, col) != (0, 0):
                            tile = self.matrix.matrix[h][d + col][w + row]
                            if isinstance(tile, Tile):
                                self.matrix.matrix[h][d + col][w + row] = False
            elif self.matrix.matrix[h][d][w].special == "":
                self.matrix.place_tile(h, d, w, special="editor_point", counts=False)
                for row in range(1, -2, -1):
                    for col in range(1, -2, -1):
                        if in_bounds(h, d + col, w + row, 
                                  self.matrix.size[2], 
                                  self.matrix.size[1], 
                                  self.matrix.size[0]):
                            tile = self.matrix.matrix[h][d + col][w + row]
                            if ((row, col) != (0, 0) and tile == False and 
                                self.matrix.can_be_placed((h, d + col, w + row))):
                                self.matrix.place_tile(h, d + col, w + row, special="editor_point", counts=False)
        self.pressed_tile = None
        self.hovered_tile = None
        super().release_left()
        
    