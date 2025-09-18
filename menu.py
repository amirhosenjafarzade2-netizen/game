# menu.py - Expanded menus with more options and submenus
import pygame
from pygame.locals import *
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_FONT_SIZE, COLOR_WHITE, COLOR_YELLOW

class Menu:
    """
    Base menu class.
    """
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, MENU_FONT_SIZE)
        self.options = []
        self.selected = 0

    def draw(self):
        self.screen.fill(COLOR_BLACK)
        for i, option in enumerate(self.options):
            color = COLOR_YELLOW if i == self.selected else COLOR_WHITE
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, 200 + i * 60))

    def handle_selection(self, keys):
        if keys[K_UP]:
            self.selected = (self.selected - 1) % len(self.options)
        if keys[K_DOWN]:
            self.selected = (self.selected + 1) % len(self.options)
        if keys[K_RETURN]:
            return self.options[self.selected].lower().replace(' ', '_')
        return None

class MainMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = ["Start Game", "Load Game", "Settings", "High Scores", "Credits", "Quit"]

class PauseMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = ["Resume", "Save Game", "Settings", "Quit to Menu"]

class SettingsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = ["Difficulty: Normal", "Sound Volume", "Music Volume", "Controls", "Back"]

    def get_selected_difficulty(self):
        # Placeholder
        return 'normal'

class HighScoreMenu(Menu):
    def draw(self, screen, scores):
        super().draw()
        for i, (score, name, date) in enumerate(scores):
            text = self.font.render(f"{i+1}. {name} - {score} ({date})", True, COLOR_WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 200, 100 + i * 40))

# Add credits menu, etc.
