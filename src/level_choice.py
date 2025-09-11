import pygame

from src.utils import *



class levelChoice(Screen):
    
    def __init__(self, screen):
        super().__init__(screen)
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.blit(TILES_TEXTURES["bg"], (0, 0))
        self.buttons["title"] = Button(self.screen, 20, 20, 60, 60, "", TILES_TEXTURES["arrow_left"])
        self.buttons["page_left"] = Button(self.screen, WIDTH // 2 - 70, HEIGHT - 80, 60, 60, "", TILES_TEXTURES["arrow_left"])
        self.buttons["page_right"] = Button(self.screen, WIDTH // 2 + 10, HEIGHT - 80, 60, 60, "", TILES_TEXTURES["arrow_right"])
        self.buttons["page_left"].active = False
        self.buttons["page_right"].active = bool(len(LEVELS.keys()) > ITEMS_PER_PAGE)
        self._page = 0
        self.add_text("page", 44, WIDTH // 2, 40, "Page 0", (255, 255, 255))
        self.reload_page()
        
    @property
    def page(self) -> int:
        return self._page
    
    @page.setter
    def page(self, p: int) -> None:
        self._page = p
        self.buttons["page_left"].active = (p != 0)
        self.buttons["page_right"].active = (p != len(LEVELS.keys()) // ITEMS_PER_PAGE)
        
    def reload_page(self) -> None:
        keys = list(LEVELS.keys())
        for i in range(ITEMS_PER_PAGE):
            if self.page * ITEMS_PER_PAGE + i < len(LEVELS.keys()):
                self.buttons[f"level{i}"] = Button(self.screen, 
                    100 + (i % ITEMS_PER_ROW) * (WIDTH // 4 + 100),
                    100 + (i // ITEMS_PER_ROW) * (HEIGHT // 4 + 100),
                    WIDTH // 4, HEIGHT // 4, "", LEVELS[keys[self.page * ITEMS_PER_PAGE + i]][1])

    def draw(self, pos):
        self.screen.blit(self.bg, (0, 0))
        return super().draw(pos)
    
    def press_left(self):
        return super().press_left()
    
    def release_left(self):
        key = super().release_left()
        if key == "page_left":
            self.page -= 1
            self.reload_page()
        elif key == "page_right":
            self.page += 1
            self.reload_page()
        elif key.startswith("level"):
            l = list(LEVELS.keys())
            return f"level:{l[self.page * ITEMS_PER_PAGE + int(key[5:])]}"
        return key
        