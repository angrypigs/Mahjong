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
        self.matrix.center_tile_matrix(
            [[[True for i in range(BOARD_WIDTH * 2 - 1)] for j in range(BOARD_DEPTH * 2 - 1)] for k in range(BOARD_HEIGHT)]
        )
        for h in range(self.matrix.size[2]):
            for d in range(self.matrix.size[1]):
                for w in range(self.matrix.size[0]):
                    self.matrix.place_tile(h, d, w, special="editor_point", info=f"{h} {d} {w}", counts=False, should_update=False)
        self.matrix.update_top_tiles()
        self.matrix.print()
        self._current_layer = 0
        self._counter = 0
        self.pressed_tile: Tile | None = None
        self.hovered_tile: Tile | None = None
        self.hovered_coords: tuple[int, int, int] | None = None
        self.buttons.append(Button(self.screen, 20, 20, 60, 60, "", TILES_TEXTURES["arrow_left"]))
        self.buttons.append(Button(self.screen, WIDTH - 80, HEIGHT // 2 - 70, 60, 60, "", TILES_TEXTURES["arrow_up"]))
        self.buttons.append(Button(self.screen, WIDTH - 80, HEIGHT // 2 + 10, 60, 60, "", TILES_TEXTURES["arrow_down"]))
        self.buttons[-1].active = False
        self.add_text("layer", 44, WIDTH // 2, 40, "Layer 0", (255, 255, 255))
        self.add_text("counter", 44, WIDTH - 20, 40, "Tiles: 0", (255, 255, 255), "midright")

    @property
    def current_layer(self) -> int:
        return self._current_layer
    
    @current_layer.setter 
    def current_layer(self, val: int) -> None:
        self._current_layer = val
        self.texts["layer"].update(text=f"Layer {val}")
        
    @property
    def counter(self) -> int:
        return self._counter
    
    @counter.setter
    def counter(self, val: int) -> None:
        self._counter = val
        self.texts["counter"].update(text=f"Tiles: {val}")
        
    def draw(self, pos) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.hovered_tile, self.hovered_coords = self.matrix.draw(pos, 
            layers=range(self._current_layer + 1), 
            active=[self._current_layer],
            show_special=[self._current_layer])
        super().draw(pos)
        
    def press_left(self):
        self.pressed_tile = self.hovered_tile
        super().press_left()
        
    def release_left(self):
        # tile input action
        if (self.pressed_tile == self.hovered_tile and self.hovered_tile is not None):
            h, d, w = self.hovered_coords
            if self.matrix.can_be_placed(self.hovered_coords):
                self.matrix.matrix[h][d][w].type = "Blank"
                self.matrix.matrix[h][d][w].counts = True
                self.matrix.matrix[h][d][w].special = ""
                self.counter += 1
                for row in range(-1, 2):
                    for col in range(-1, 2):
                        if in_bounds(h, d + col, w + row, 
                                  self.matrix.size[2], 
                                  self.matrix.size[1], 
                                  self.matrix.size[0]) and (row, col) != (0, 0):
                            tile = self.matrix.matrix[h][d + col][w + row]
                            if isinstance(tile, Tile):
                                self.matrix.matrix[h][d + col][w + row] = False
            elif (self.matrix.matrix[h][d][w].special == "" and 
                  h == self.current_layer and
                  self.matrix.can_be_removed((h, d, w), both_cons=False)):
                self.matrix.place_tile(h, d, w, special="editor_point", counts=False)
                self.counter -= 1
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
        key = super().release_left()
        # input actions (up / down)
        if key == 1: # up
            self.current_layer = min(self._current_layer + 1, BOARD_HEIGHT - 1)
            self.buttons[-2].active = not (self._current_layer == BOARD_HEIGHT - 1)
            self.buttons[-1].active = not (self._current_layer == 0)
            for d in range(self.matrix.size[1]):
                for w in range(self.matrix.size[0]):
                    tile = self.matrix.matrix[self._current_layer][d][w]
                    tile_lower = self.matrix.matrix[self._current_layer - 1][d][w]
                    if isinstance(tile, Tile) and not tile.special:
                        tile.type = "Blank"
                    elif self.matrix.can_be_placed((self._current_layer, d, w), both_cons=False):
                        self.matrix.place_tile(self._current_layer, d, w, special="editor_point", counts=False, should_update=False)
                    else:
                        self.matrix.matrix[self._current_layer][d][w] = False
                    if isinstance(tile_lower, Tile) and not tile_lower.special:
                        tile_lower.type = "Blocked"
        elif key == 2: # down
            self.current_layer = max(self._current_layer - 1, 0)
            self.buttons[-2].active = not (self._current_layer == BOARD_HEIGHT - 1)
            self.buttons[-1].active = not (self._current_layer == 0)
            for d in range(self.matrix.size[1]):
                for w in range(self.matrix.size[0]):
                    tile = self.matrix.matrix[self._current_layer][d][w]
                    if isinstance(tile, Tile) and not tile.special:
                        tile.type = "Blank"
        return 0 if key == 0 else None
        
    