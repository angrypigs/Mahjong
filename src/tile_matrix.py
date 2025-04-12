import pygame

import random
from copy import deepcopy

from src.utils import *
from src.tile import Tile



class tileMatrix:
    """
    Class of tile matrix

    Args:
        size: (width, depth, height)
    """
    def __init__(self, screen: pygame.Surface, size: tuple[int, int, int]) -> None:
        self.screen = screen
        self.quantity = 0
        self.size = (size[0] * 2 - 1, size[1] * 2 - 1, size[2])
        self._matrix : list[list[list[Tile | bool]]] = [[[False for _ in range(self.size[0])]
                                                        for _ in range(self.size[1])]
                                                       for _ in range(self.size[2])]
        
    def generate_board(self, places: list[list[list[bool]]]) -> None:
        keys = list(TILES_TEXTURES["Dark"].keys())
        keys = [x for x in keys for _ in range(4)]
        random.shuffle(keys)
        self._matrix = deepcopy(places)
        self.quantity = len(keys)
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    if self._matrix[h][d][w]:
                        self._matrix[h][d][w] = Tile(self.screen, 
                                                    WIDTH // 2 - TILE_WIDTH * self.size[0] // 4 + TILE_WIDTH * w - TILE_HEIGHT * h, 
                                                    HEIGHT // 2 - TILE_DEPTH * self.size[1] // 4 + TILE_DEPTH * d - TILE_HEIGHT * h - 100,
                                                    keys.pop(), "Dark")
        
    def print(self) -> None:
        print(len(self._matrix), len(self._matrix[0]), len(self._matrix[0][0]))
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                print(self._matrix[h][d])
            print("\n") 
    
    def draw(self, pos) -> Tile | None:
        over = None
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    if type(self._matrix[h][d][w]) == Tile:
                        if self._matrix[h][d][w].draw(pos):
                            over = self._matrix[h][d][w]
        return over
    
    def remove_tiles(self, tiles: list[Tile]) -> None:
        q = len(tiles)
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    for tile in tiles:
                        if tile == self._matrix[h][d][w]:
                            self._matrix[h][d][w] = True
                            tiles.remove(tile)
                            if not tiles:
                                self.quantity -= q
                                return
    
        