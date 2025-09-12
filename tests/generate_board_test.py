from src.tile_matrix import tileMatrix
from src.utils import *
import pygame

def generate_board_test(uuid: str) -> None:
    screen = pygame.Surface((WIDTH, HEIGHT))
    matrix = tileMatrix(screen, (BOARD_WIDTH, BOARD_DEPTH, BOARD_HEIGHT))
    m = LEVELS[uuid][0]
    for _ in range(10000):
        n = matrix.generate_board(m)
        if n != 90:
            matrix.print()