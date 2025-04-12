import pygame

from src.utils import *


class Tile:
    
    def __init__(self, screen: pygame.Surface, 
                 x: int, y: int,
                 tile_type: str,
                 color: str) -> None:
        self.screen = screen
        self.type = tile_type
        self.color = color
        self.coords = pygame.math.Vector2(x, y)
        self.rect = TILES_TEXTURES[self.color][tile_type].get_rect(topleft=self.coords)
        self.selected = False
        
    def __str__(self) -> str:
        return f"Tile {self.coords.x} {self.coords.y} {self.type}"
        
    def draw(self, pos) -> bool:
        is_over = self.rect.collidepoint(pos)
        color = self.color + ("Selected" if is_over or self.selected else "")
        self.screen.blit(TILES_TEXTURES[color][self.type], self.coords)
        return is_over
        
    
    