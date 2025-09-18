# config.py - Expanded config with more settings
from constants import DIFFICULTY_NORMAL

class Config:
    """
    Game configuration.
    """
    def __init__(self):
        self.difficulty = 'normal'
        self.sound_volume = 1.0
        self.music_volume = 0.8
        self.fullscreen = False
        self.key_bindings = {
            'left': K_LEFT,
            'right': K_RIGHT,
            'up': K_UP,
            'down': K_DOWN,
            'shoot': K_SPACE
        }

    def get_difficulty(self):
        if self.difficulty == 'easy':
            return DIFFICULTY_EASY
        elif self.difficulty == 'hard':
            return DIFFICULTY_HARD
        return DIFFICULTY_NORMAL

    def set_difficulty(self, diff):
        self.difficulty = diff

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        # Apply fullscreen mode placeholder
