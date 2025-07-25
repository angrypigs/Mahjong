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
        self.offset_x = 0
        self.offset_y = 0
        self._top_tiles: list[tuple[int, int, int]] = []
        print(self.size)
        self.matrix : list[list[list[Tile | bool]]] = [[[False for _ in range(self.size[0])]
                                                        for _ in range(self.size[1])]
                                                       for _ in range(self.size[2])]
        
    def generate_board(self, places: list[list[list[bool]]]) -> None:
        keys = [x for x in TILES_TEXTURES["Dark"].keys() if x != "Blank"]
        keys = [x for x in keys for _ in range(2)]
        # print(keys)
        random.shuffle(keys)
        self.matrix = deepcopy(places)
        self.quantity = len(keys) * 2
        counter = len(keys)
        self.__center_tile_matrix(places)
        coords = []
        err_blocks = []
        while counter > 0:
            new_places = []
            all_places = []
            for h in reversed(range(self.size[2])):
                for d in range(self.size[1]):
                    for w in range(self.size[0]):
                        if self.matrix[h][d][w] == True:
                            all_places.append((h, d, w))
                            if self.can_be_removed((h, d, w), True):
                                new_places.append((h, d, w))
            try:
                two_places = random.sample(new_places, 2)
            except ValueError:
                err_blocks = all_places.copy()
                break
            for h, d, w in two_places:
                self.matrix[h][d][w] = False
            two_places.append(keys.pop())
            coords.append(two_places)
            counter -= 1
        if err_blocks:
            print(len(coords))
            other_blocks = []
            err_coords = err_blocks[0][1:]
            while len(err_blocks) != len(other_blocks):
                b1, b2, key = coords.pop()
                keys.append(key)
                blocks = [b1, b2]
                for b in blocks:
                    if (b[1], b[2]) == err_coords:
                        err_blocks.append(b)
                    else:
                        other_blocks.append(b)
            err_blocks.sort(key=lambda x: x[0], reverse=True)
            other_blocks.sort(key=lambda x: x[0], reverse=True)
            for i in range(len(err_blocks)):
                coords.append((err_blocks[i], other_blocks[i], keys.pop()))
            print(len(coords))
        for c in coords:
            c1, c2, key = c
            for h, d, w in (c1, c2):
                self.place_tile(h, d, w, key, info=f"{h} {d} {w}", should_update=False)
        self.update_top_tiles()
     
    def print(self) -> None:
        print(len(self.matrix), len(self.matrix[0]), len(self.matrix[0][0]))
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                line = []
                for w in range(self.size[0]):
                    match self.matrix[h][d][w]:
                        case False:
                            line.append('0')
                        case True:
                            line.append('1')
                        case _:
                            line.append('2')
                print(" ".join(line))  
            print("\n") 
    
    def draw(self, pos, layers: list[int] | None = None, active: bool = True
             ) -> tuple[Tile, tuple[int, int, int]] | tuple[None, None]:
        """
        Draws the matrix
    
        Args:
            pos: cursor position
            layers (list[int] | None): optional list of indexes of layers to be shown
            active (bool): whether tiles should react to cursor
            
        Returns:
            tuple[Tile, tuple[int, int, int]] | tuple[None, None]: Tile and it's coords if one's under cursor, None vals oth.
        """
        over = [None, None]
        for h in range(self.size[2]) if layers is None else layers:
            for d in range(self.size[1] - 1, -1, -1):
                for w in range(self.size[0] - 1, -1, -1):
                    if type(self.matrix[h][d][w]) == Tile:
                        if self.matrix[h][d][w].draw(pos, 
                            active and (h, d, w) in self._top_tiles):
                            over = (self.matrix[h][d][w], (h, d, w))
        return over
    
    def remove_tiles(self, tiles: list[Tile]) -> None:
        q = len(tiles)
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    for tile in tiles:
                        if tile == self.matrix[h][d][w]:
                            self.matrix[h][d][w] = True
                            tiles.remove(tile)
                            if not tiles:
                                self.quantity -= q
                                self.update_top_tiles()
                                return
                            
    def place_tile(self, h: int, d: int, w: int,
                   key: str = "1-a", color: str = "Dark", 
                   special: str = "", info: str = "",
                   counts: bool = True,
                   should_update: bool = True) -> None:
        x = w * TILE_WIDTH + self.offset_x - TILE_HEIGHT * h
        y = d * TILE_DEPTH + self.offset_y - TILE_HEIGHT * h
        self.matrix[h][d][w] = Tile(self.screen, x, y, key, color, special, info, counts)
        if should_update: self.update_top_tiles()
    
    def can_be_removed(self, coords: tuple[int, int, int],
                       true_included: bool = False) -> bool:
        h, d, w = coords
        side_counter = 0
        for col_w in [w - 2, w + 2]:
            for row_add in range(-1, 2):
                if in_bounds(h, d + row_add, col_w, self.size[2], self.size[1], self.size[0]):
                    if (isinstance(self.matrix[h][d + row_add][col_w], Tile) or
                        true_included and self.matrix[h][d + row_add][col_w] == True):
                        side_counter += 1
                        break
        if side_counter == 2:
            return False
        for h_add in range(1, self.size[2] - h):
            for row_add in range(-1, 2):
                for col_add in range(-1, 2):
                    if in_bounds(h + h_add, d + row_add, w + col_add, self.size[2], self.size[1], self.size[0]):
                        if (isinstance(self.matrix[h + h_add][d + row_add][w + col_add], Tile) or
                            true_included and self.matrix[h + h_add][d + row_add][w + col_add] == True):
                            return False
        return True
    
    def can_be_placed(self, coords: tuple[int, int, int]) -> bool:
        h, d, w = coords
        for row_add in range(-1, 2):
            for col_add in range(-1, 2):
                if in_bounds(h, d + col_add, w + row_add, self.size[2], self.size[1], self.size[0]):
                    if (isinstance(self.matrix[h][d + col_add][w + row_add], Tile) and 
                        not self.matrix[h][d + col_add][w + row_add].special):
                        return False
        if h == 0:
            return True
        for row_add in range(-1, 2):
            for col_add in range(-1, 2):
                if in_bounds(h - 1, d + col_add, w + row_add, self.size[2], self.size[1], self.size[0]):
                    if (isinstance(self.matrix[h - 1][d + col_add][w + row_add], Tile) and
                        not self.matrix[h - 1][d + col_add][w + row_add].special):
                        return True
        return False
    
    def update_top_tiles(self) -> None:
        self._top_tiles = []
        for h in range(self.size[2] - 1, -1, -1):
            for d in range(self.size[1] - 1, -1, -1):
                for w in range(self.size[0] - 1, -1, -1):
                    if self.can_be_removed((h, d, w)):
                        self._top_tiles.append((h, d, w))
    
    def __neighbor_counter(self, coords: tuple[int, int, int]) -> int:
        h, d, w = coords
        counter = 0
        for col_w in [w - 2, w + 2]:
            for row_add in range(-1, 2):
                if in_bounds(h, d + row_add, col_w, self.size[2], self.size[1], self.size[0]):
                    if isinstance(self.matrix[h][d + row_add][col_w], Tile):
                        counter += 1
        return counter
    
    def __center_tile_matrix(self, places: list[list[list[bool]]]) -> None:
        limits_x = [self.size[0] - 1, 0]
        limits_y = [self.size[1] - 1, 0]
        for h in range(self.size[2]):
            for d in range(self.size[1]):
                for w in range(self.size[0]):
                    if places[h][d][w]:
                        if w < limits_x[0]:
                            limits_x[0] = w
                        if w > limits_x[1]:
                            limits_x[1] = w
                        if d < limits_y[0]:
                            limits_y[0] = d
                        if d > limits_y[1]:
                            limits_y[1] = d
        w = limits_x[1] - limits_x[0]
        d = limits_y[1] - limits_y[0]
        center_x = (limits_x[0] + w / 2) * TILE_WIDTH
        center_y = (limits_y[0] + d / 2) * TILE_DEPTH
        self.offset_x = WIDTH / 2 - center_x
        self.offset_y = HEIGHT / 2 - center_y
        