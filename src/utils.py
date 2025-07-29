import pygame

import os
import sys

HEIGHT = 700
WIDTH = 1000
FPS = 90

BOARD_WIDTH = 15
BOARD_DEPTH = 8
BOARD_HEIGHT = 5

SCALE_FACTOR = (2, 8)

TILE_WIDTH = 100 * SCALE_FACTOR[0] // SCALE_FACTOR[1]
TILE_DEPTH = 133 * SCALE_FACTOR[0] // SCALE_FACTOR[1]
TILE_HEIGHT = 14 * SCALE_FACTOR[0] // SCALE_FACTOR[1]

BTN_COLOR = (40, 40, 40)
BTN_COLOR_ACTIVE = (70, 70, 70)

CLICK_STATES = {
    "title": {
        0: "game",
        1: "editor"
    },
    "game": {
        0: "title"
    },
    "editor": {
        0: "title"
    }
}

MODEL1 = [[[bool((i % 6 == 0 or i % 6 == 2) and j % 2 == 0 and i < 18 and j < 12) for i in range(BOARD_WIDTH * 2 - 1)]
                  for j in range(BOARD_DEPTH * 2 - 1)]
                 for k in range(BOARD_HEIGHT)]

MODEL2 = [[[bool(i % 2 == 0 and j % 2 == 0 and i < 12 and j < 12) for i in range(BOARD_WIDTH * 2 - 1)]
                  for j in range(BOARD_DEPTH * 2 - 1)]
                 for k in range(BOARD_HEIGHT)]

MODEL3 = [[[bool(i % 4 == 0 and j % 2 == 0 and i < 23 and j < 12) for i in range(BOARD_WIDTH * 2 - 1)]
                  for j in range(BOARD_DEPTH * 2 - 1)]
                 for k in range(BOARD_HEIGHT)]

def in_bounds(h, d, w, h_max, d_max, w_max) -> bool:
    return 0 <= h < h_max and 0 <= d < d_max and 0 <= w < w_max

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
        self.active = True

    def draw(self, cursor_pos) -> bool:
        if self.active:
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
        self.buttons: list[Button] = []
        self._hovered_button: int | None = None
        self._pressed_button: int | None = None

    def draw(self, pos: tuple[int, int]) -> None:
        self._hovered_button = None
        for i, button in enumerate(self.buttons):
            if button.draw(pos):
                self._hovered_button = i
    
    def press_left(self) -> None:
        self._pressed_button = self._hovered_button
    
    def release_left(self) -> int | None:
        res = None
        if self._hovered_button == self._pressed_button and self._hovered_button is not None:
            res = self._hovered_button
        self._pressed_button = None
        self._hovered_button = None
        return res
        

def res_path(rel_path: str) -> str:
    """
    Return path to file modified by auto_py_to_exe path if packed to exe already
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = sys.path[0]
    return os.path.normpath(os.path.join(base_path, rel_path))

TILES_TEXTURES : dict[str, dict[str, pygame.Surface]] = {
    "Dark": {},
    "DarkSelected": {},
    "Light": {},
    "LightSelected": {}
}

def init_assets() -> None:
    TILES_TEXTURES["bg"] = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(res_path("assets/Background & Shadow"), "Background Green.png")), (WIDTH, HEIGHT))
    for name in ["editor_point"]:
        image = pygame.image.load(res_path(f"assets/Other/{name}.png"))
        width, height = image.get_size()
        TILES_TEXTURES[name] = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1] // 2, 
                                                                        height * SCALE_FACTOR[0] // SCALE_FACTOR[1] // 2))
    image = pygame.image.load(res_path(f"assets/Dark Theme/Neutral Blank.png"))
    width, height = image.get_size()
    TILES_TEXTURES["blank_dark"] = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1], 
                                                                    height * SCALE_FACTOR[0] // SCALE_FACTOR[1]))
    image = pygame.image.load(res_path(f"assets/Light Theme/Neutral Blank.png"))
    width, height = image.get_size()
    TILES_TEXTURES["blank_light"] = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1], 
                                                                    height * SCALE_FACTOR[0] // SCALE_FACTOR[1]))
    for filename in os.listdir(res_path("assets/Buttons")):
        key = filename.removesuffix(".png")
        image_path = os.path.join(res_path("assets/Buttons"), filename)
        TILES_TEXTURES[key] = pygame.transform.smoothscale(pygame.image.load(image_path), (80, 80))
    for filename in os.listdir(res_path("assets/Dark Theme")):
        if filename.startswith("Neutral"):
            key = filename.removeprefix("Neutral ").removesuffix(".png")
            # if key != "Blank":
            image_path = os.path.join(res_path("assets/Dark Theme"), filename)
            image = pygame.image.load(image_path)
            width, height = image.get_size()
            scaled_image = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1], 
                                                                height * SCALE_FACTOR[0] // SCALE_FACTOR[1]))
            TILES_TEXTURES["Dark"][key] = scaled_image
        elif filename.startswith("Selected"):
            key = filename.removeprefix("Selected ").removesuffix(".png")
            # if key != "Blank":
            image_path = os.path.join(res_path("assets/Dark Theme"), filename)
            image = pygame.image.load(image_path)
            width, height = image.get_size()
            scaled_image = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1], 
                                                                height * SCALE_FACTOR[0] // SCALE_FACTOR[1]))
            TILES_TEXTURES["DarkSelected"][key] = scaled_image