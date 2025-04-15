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
        print(self.size)
        self._matrix : list[list[list[Tile | bool]]] = [[[False for _ in range(self.size[0])]
                                                        for _ in range(self.size[1])]
                                                       for _ in range(self.size[2])]
        
    def generate_board(self, places: list[list[list[bool]]]) -> None:
        keys = list(TILES_TEXTURES["Dark"].keys())
        keys = [x for x in keys for _ in range(2)]
        random.shuffle(keys)
        self._matrix = deepcopy(places)
        self.quantity = len(keys) * 2
        for i in range(len(keys)):
            iter_places = []
            for h in range(self.size[2]):
                for d in range(self.size[1]):
                    for w in range(self.size[0]):
                        if self._matrix[h][d][w] == True and self.can_be_placed((h, d, w)) and self.can_be_removed((h, d, w)):
                            iter_places.append(((h, d, w), self.__neighbor_counter((h, d, w))))
            best_places = []
            for p in sorted(iter_places, key=lambda x: x[1], reverse=True):
                if len(best_places) < 2 or p[1] == best_places[0][1]:
                    best_places.append(p)
                else:
                    break
            key = keys.pop()
            for p in random.sample(best_places, 2):
                h, d, w = p[0]
                self._matrix[h][d][w] = Tile(self.screen, 
                                            WIDTH // 2 - TILE_WIDTH * self.size[0] // 4 + TILE_WIDTH * w - TILE_HEIGHT * h, 
                                            HEIGHT // 2 - TILE_DEPTH * self.size[1] // 4 + TILE_DEPTH * d - TILE_HEIGHT * h - 100,
                                            key, "Dark")
        
    def print(self) -> None:
        print(len(self._matrix), len(self._matrix[0]), len(self._matrix[0][0]))
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                print(self._matrix[h][d])
            print("\n") 
    
    def draw(self, pos) -> tuple[Tile, tuple[int, int, int]] | tuple[None, None]:
        over = [None, None]
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    if type(self._matrix[h][d][w]) == Tile:
                        if self._matrix[h][d][w].draw(pos):
                            over = (self._matrix[h][d][w], (h, d, w))
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
    
    def can_be_removed(self, coords: tuple[int, int, int],
                       true_included: bool = False) -> bool:
        h, d, w = coords
        side_counter = 0
        for col_w in [w - 2, w + 2]:
            for row_add in range(-1, 2):
                if in_bounds(h, d + row_add, col_w, self.size[2], self.size[1], self.size[0]):
                    if (isinstance(self._matrix[h][d + row_add][col_w], Tile) or
                        true_included and self._matrix[h][d + row_add][col_w] == True):
                        side_counter += 1
                        break
        if side_counter == 2:
            return False
        for row_add in range(-1, 2):
            for col_add in range(-1, 2):
                if in_bounds(h + 1, d + row_add, w + col_add, self.size[2], self.size[1], self.size[0]):
                    if isinstance(self._matrix[h + 1][d + row_add][w + col_add], Tile):
                        return False
        return True
    
    def can_be_placed(self, coords: tuple[int, int, int]) -> bool:
        h, d, w = coords
        for row_add in range(-1, 2):
            for col_add in range(-1, 2):
                if in_bounds(h, d + col_add, w + row_add, self.size[2], self.size[1], self.size[0]):
                    if isinstance(self._matrix[h][d + col_add][w + row_add], Tile):
                        return False
        if h == 0:
            return True
        for row_add in range(-1, 2):
            for col_add in range(-1, 2):
                if in_bounds(h - 1, d + col_add, w + row_add, self.size[2], self.size[1], self.size[0]):
                    if isinstance(self._matrix[h - 1][d + col_add][w + row_add], Tile):
                        return True
        return False
    
    def __neighbor_counter(self, coords: tuple[int, int, int]) -> int:
        h, d, w = coords
        counter = 0
        for col_w in [w - 2, w + 2]:
            for row_add in range(-1, 2):
                if in_bounds(h, d + row_add, col_w, self.size[2], self.size[1], self.size[0]):
                    if isinstance(self._matrix[h][d + row_add][col_w], Tile):
                        counter += 1
        return counter
        