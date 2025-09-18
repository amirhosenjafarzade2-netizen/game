# score_system.py - Expanded scoring with bonuses
from constants import SCORE_MULTIPLIER

class ScoreSystem:
    """
    Manages scoring and multipliers.
    """
    def __init__(self):
        self.score = 0
        self.multiplier = 1.0
        self.combo = 0
        self.combo_timeout = 2000
        self.last_kill = 0

    def reset(self):
        self.score = 0
        self.multiplier = 1.0
        self.combo = 0

    def add_score(self, value):
        self.score += int(value * self.multiplier)
        self.combo += 1
        self.last_kill = pygame.time.get_ticks()
        if self.combo % 5 == 0:
            self.multiplier += 0.1

    def check_combo(self):
        now = pygame.time.get_ticks()
        if now - self.last_kill > self.combo_timeout:
            self.combo = 0
            self.multiplier = 1.0

    def update(self):
        self.check_combo()
