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
        
    def draw(self, pos) -> None:
        color = self.color + ("Selected" if self.rect.collidepoint(pos) else "")
        self.screen.blit(TILES_TEXTURES[color][self.type], self.coords)
        
    
    