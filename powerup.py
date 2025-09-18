# powerup.py - Expanded with more powerup types
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, POWERUP_SPEED, COLOR_GREEN, COLOR_BLUE, COLOR_YELLOW, COLOR_RED, COLOR_ORANGE

class PowerUp(pygame.sprite.Sprite):
    """
    Base powerup class.
    """
    def __init__(self, type='health'):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        colors = {
            'health': COLOR_GREEN,
            'shield': COLOR_BLUE,
            'speed': COLOR_YELLOW,
            'weapon': COLOR_RED,
            'life': COLOR_ORANGE,
            'invincibility': COLOR_PURPLE,
            'score': COLOR_CYAN,
            'magnet': COLOR_WHITE,
            'bomb': COLOR_RED
        }
        self.image.fill(colors.get(type, COLOR_WHITE))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-200, -50)

    def update(self):
        self.rect.y += POWERUP_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def apply(self, player):
        player.apply_powerup(self.type)

# Subclasses for each type
class ShieldPowerUp(PowerUp):
    def __init__(self):
        super().__init__('shield')

class SpeedPowerUp(PowerUp):
    def __init__(self):
        super().__init__('speed')

class WeaponPowerUp(PowerUp):
    def __init__(self):
        super().__init__('weapon')

class LifePowerUp(PowerUp):
    def __init__(self):
        super().__init__('life')

class InvincibilityPowerUp(PowerUp):
    def __init__(self):
        super().__init__('invincibility')

class ScorePowerUp(PowerUp):
    def __init__(self):
        super().__init__('score')

class MagnetPowerUp(PowerUp):
    def __init__(self):
        super().__init__('magnet')

class BombPowerUp(PowerUp):
    def __init__(self):
        super().__init__('bomb')

# Add more if needed
