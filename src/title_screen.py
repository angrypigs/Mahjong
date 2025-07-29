import pygame

from src.utils import *



class titleScreen(Screen):
    
    def __init__(self, screen):
        super().__init__(screen)
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.blit(TILES_TEXTURES["bg"], (0, 0))
        w = 300
        h = 60
        self.buttons.append(Button(self.screen, (WIDTH - w) // 2, (HEIGHT - h) // 2 - 50,
                                    w, h, "Play"))
        self.buttons.append(Button(self.screen, (WIDTH - w) // 2, (HEIGHT - h) // 2 + 50,
                                    w, h, "Editor"))
        
    def draw(self, pos):
        self.screen.blit(self.bg, (0, 0))
        return super().draw(pos)
    
    def press_left(self):
        return super().press_left()
    
    def release_left(self):
        return super().release_left()