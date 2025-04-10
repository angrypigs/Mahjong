import pygame

from os import path
import sys

HEIGHT = 700
WIDTH = 1000
FPS = 90

BTN_COLOR = (40, 40, 40)
BTN_COLOR_ACTIVE = (70, 70, 70)

class Button:

    def __init__(self, screen: pygame.Surface,
                 x: int, 
                 y: int, 
                 width: int, 
                 height: int, 
                 text: str,
                 img: pygame.Surface | None = None,
                 color: tuple[int, int, int] | None = None) -> None:
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 44)
        self._cursor_flag = False
        self.img = pygame.transform.scale(img, (width, height)) if img is not None else None
        self.color = BTN_COLOR if color is None else color
        self.color_active = BTN_COLOR_ACTIVE if color is None else tuple([x + 40 for x in color])

    def draw(self, cursor_pos) -> bool:
        pygame.draw.rect(self.screen, 
                         self.color_active if self._cursor_flag else self.color, 
                         self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, (204, 204, 204))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)
        if self.img is not None:
            self.screen.blit(self.img, (self.rect))
        if self.rect.collidepoint(cursor_pos):
            self._cursor_flag = True
            return True
        else:
            self._cursor_flag = False
            return False
        
class Screen:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def draw(self, pos: tuple[int, int]) -> None:
        raise NotImplementedError()
        

def res_path(rel_path: str) -> str:
    """
    Return path to file modified by auto_py_to_exe path if packed to exe already
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = sys.path[0]
    return path.normpath(path.join(base_path, rel_path))