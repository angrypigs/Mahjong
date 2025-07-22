import pygame

from src.utils import *


class Tile:
    
    def __init__(self, screen: pygame.Surface, 
                 x: int, y: int,
                 tile_type: str = "",
                 color: str = "Dark",
                 _special_type: str = "",
                 info: str = "",
                 counts: bool = True) -> None:
        """
        Tile init

        Args:
            screen (Surface): origin screen.
            x (int): world x.
            y (int): world y.
            tile_type (str): tile name from file.
            color (str): color mode, "Dark" | "Light".
            _special_type (str): name of the texture to not take from Dark / Light.
            info (str): opt. info.
            counts (bool): internal flag, for specific uses.
        """
        self.screen = screen
        self.counts = counts
        self.type = tile_type
        self._special = _special_type
        self.color = color
        self.info = info
        self.coords = pygame.math.Vector2(x, y)
        if self._special:
            self.rect = TILES_TEXTURES[self._special].get_rect(topleft=self.coords)
        else:
            self.rect = TILES_TEXTURES[self.color][tile_type].get_rect(topleft=self.coords)
        self.selected = False
        
    def __str__(self) -> str:
        return f"Tile {self.coords.x} {self.coords.y} {self.type} {self.info}"
        
    def draw(self, pos) -> bool:
        is_over = self.rect.collidepoint(pos)
        color = self.color + ("Selected" if is_over or self.selected else "")
        self.screen.blit(TILES_TEXTURES[color][self.type] if not self._special else 
                         TILES_TEXTURES[self._special], self.coords)
        return is_over
    
    @property
    def special(self) -> str:
        return self._special
    
    @special.setter
    def special(self, val) -> None:
        print(f"new val: {val}")
        self._special = val
        
    
    