import pygame

from src.utils import *
from src.tile_matrix import tileMatrix
from src.tile import Tile



class Game(Screen):
    
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.matrix = tileMatrix(self.screen, (BOARD_WIDTH, BOARD_DEPTH, BOARD_HEIGHT))
        board = [[[bool(i % 2 == 0 and j % 2 == 0 and k == 0 and i < 20) for i in range(BOARD_WIDTH * 2 - 1)]
                  for j in range(BOARD_DEPTH * 2 - 1)]
                 for k in range(BOARD_HEIGHT)]
        self.matrix.generate_board(board)
        
        
    def draw(self, pos) -> None:
        self.matrix.draw(pos)