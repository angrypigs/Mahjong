import pygame

from src.utils import *
from src.game import Game



class Window:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Madżong")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_mode = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False