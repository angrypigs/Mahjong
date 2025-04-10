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
        self.size = (size[0] * 2 - 1, size[1] * 2 - 1, size[2])
        self.matrix : list[list[list[Tile | bool]]] = [[[False for _ in range(self.size[0])]
                                                        for _ in range(self.size[1])]
                                                       for _ in range(self.size[2])]
        
    def generate_board(self, places: list[list[list[bool]]]) -> None:
        keys = list(TILES_TEXTURES["Dark"].keys())
        keys = [x for x in keys for _ in range(4)]
        random.shuffle(keys)
        print(keys)
        self.matrix = deepcopy(places)
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    if self.matrix[h][d][w]:
                        self.matrix[h][d][w] = Tile(self.screen, 100 + TILE_WIDTH * w, 100 + TILE_DEPTH * d,
                                                    keys.pop(), "Dark")
        
    def print(self) -> None:
        print(len(self.matrix), len(self.matrix[0]), len(self.matrix[0][0]))
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                print(self.matrix[h][d])
            print("\n")
                    
    
    def draw(self, pos) -> None:
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    if type(self.matrix[h][d][w]) == Tile:
                        self.matrix[h][d][w].draw(pos)
        