import pygame

import os
import sys
from typing import Optional, Literal
from pathlib import Path

HEIGHT = 700
WIDTH = 1000
FPS = 90

SETTINGS = {
    "Theme": "Dark"
}

BOARD_WIDTH = 15
BOARD_DEPTH = 8
BOARD_HEIGHT = 5

SCALE_FACTOR = (2, 8)

TILE_WIDTH = 101 * SCALE_FACTOR[0] // SCALE_FACTOR[1]
TILE_DEPTH = 134 * SCALE_FACTOR[0] // SCALE_FACTOR[1]
TILE_HEIGHT = 15 * SCALE_FACTOR[0] // SCALE_FACTOR[1]

ITEMS_PER_PAGE = 6
ITEMS_PER_ROW = 3

COLORS = {
    "Dark": {
        "Normal": (40, 40, 40),
        "Active": (70, 70, 70),
        "Text": (204, 204, 204),
        "Overlay": (204, 204, 204)
    },
    "Light": {
        "Normal": (170, 170, 130),
        "Active": (200, 200, 150),
        "Text": (20, 20, 20),
        "Overlay": (20, 20, 20)
    }
}

if os.name == "nt":  # Windows
    ROAMING_PATH = Path(os.environ['APPDATA']) / "MahjongPython"
else:  # Linux / macOS
    ROAMING_PATH = Path.home() / ".config" / "MahjongPython"
    
LEVELS: dict[str, list[list[list[list[bool]]], pygame.Surface]] = {}

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
                 img: pygame.Surface | None = None) -> None:
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 44)
        self._cursor_flag = False
        self.img = pygame.transform.smoothscale(img, (width, height)) if img is not None else None
        self.reload()
        self.active = True
        
    def reload(self) -> None:
        self.color = COLORS[SETTINGS["Theme"]]["Normal"]
        self.color_active = COLORS[SETTINGS["Theme"]]["Active"]
        self.text_color = COLORS[SETTINGS["Theme"]]["Text"]

    def draw(self, cursor_pos) -> bool:
        if self.active:
            pygame.draw.rect(self.screen, 
                            self.color_active if self._cursor_flag else self.color, 
                            self.rect, border_radius=10)
            text_surface = self.font.render(self.text, True, self.text_color)
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
           
Alignment = Literal[
    "center", "topleft", "topcenter", 
    "midleft", "midright", "bottomleft", 
    "bottomright", "bottomcenter"
]
            
class Font:
    
    def __init__(self, parent, text: str, size: int, 
                 x: int, y: int, 
                 color: tuple[int, int, int],
                 align: Alignment = "center") -> None:
        self.parent = parent
        self.align = align
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.color = color
        self.font: pygame.Surface = self.parent.fonts[size].render(self.text, True, self.color)
        self.rect = self._get_rect()
        
    def _get_rect(self) -> pygame.Rect:
        rect = self.font.get_rect()
        setattr(rect, self.align, (self.x, self.y))
        return rect
        
    def update(self, text: Optional[str] = None,
               x: Optional[int] = None,
               y: Optional[int] = None,
               size: Optional[int] = None,
               color: Optional[tuple[int, int, int]] = None) -> None:
        if text is not None:
            self.text = text
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if size is not None:
            self.size = size
        if color is not None:
            self.color = color
        self.font: pygame.Surface = self.parent.fonts[self.size].render(self.text, True, self.color)
        self.rect = self._get_rect()
        
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.font, self.rect)
        
class Screen:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.buttons: dict[str, Button] = {}
        self._hovered_button: str | None = None
        self._pressed_button: str | None = None
        self.fonts: dict[int, pygame.font.Font] = {}
        self.texts: dict[str, Font] = {}
        
    def add_text(self, 
                 name: str,
                 size: int,
                 x: int, 
                 y: int, 
                 text: str,
                 color: tuple[int, int, int] = (0, 0, 0),
                 align: Alignment = "center"
        ) -> None:
        if size not in self.fonts.keys():
            self.fonts[size] = pygame.font.Font(None, size)
        self.texts[name] = Font(self, text, size, x, y, color, align)

    def draw(self, pos: tuple[int, int]) -> None:
        self._hovered_button = None
        for key, button in self.buttons.items():
            if button.draw(pos):
                self._hovered_button = key
        for f in self.texts.values():
            f.draw(self.screen)
    
    def press_left(self) -> None:
        self._pressed_button = self._hovered_button
    
    def release_left(self) -> str | None:
        res = None
        if self._hovered_button == self._pressed_button and self._hovered_button is not None:
            res = self._hovered_button
        self._pressed_button = None
        self._hovered_button = None
        return res
    
    def reload(self) -> None:
        for button in self.buttons.values():
            button.reload()
        

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
    "LightSelected": {},
    "quantity": 0
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
    for theme in ("Dark", "Light"):
        for filename in os.listdir(res_path(f"assets/{theme} Theme")):
            if filename.startswith("Neutral"):
                key = filename.removeprefix("Neutral ").removesuffix(".png")
                # if key != "Blank":
                image_path = os.path.join(res_path(f"assets/{theme} Theme"), filename)
                image = pygame.image.load(image_path)
                width, height = image.get_size()
                scaled_image = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1], 
                                                                    height * SCALE_FACTOR[0] // SCALE_FACTOR[1]))
                TILES_TEXTURES[theme][key] = scaled_image.copy()
            elif filename.startswith("Selected"):
                key = filename.removeprefix("Selected ").removesuffix(".png")
                # if key != "Blank":
                image_path = os.path.join(res_path(f"assets/{theme} Theme"), filename)
                image = pygame.image.load(image_path)
                width, height = image.get_size()
                scaled_image = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1], 
                                                                    height * SCALE_FACTOR[0] // SCALE_FACTOR[1]))
                TILES_TEXTURES[f"{theme}Selected"][key] = scaled_image.copy()
        image = pygame.image.load(res_path(f"assets/Other/{theme}Overlay.png")).convert_alpha()
        width, height = image.get_size()
        scaled_image = pygame.transform.smoothscale(image, (width * SCALE_FACTOR[0] // SCALE_FACTOR[1], 
                                                            height * SCALE_FACTOR[0] // SCALE_FACTOR[1]))
        TILES_TEXTURES[f"{theme}Overlay"] = scaled_image.copy()
    TILES_TEXTURES["quantity"] = len([x for x in TILES_TEXTURES["Dark"].keys() if x not in ["Blank", "Blocked"]]) * 4
    levels_path = ROAMING_PATH / "levels"
    levels_path.mkdir(parents=True, exist_ok=True)