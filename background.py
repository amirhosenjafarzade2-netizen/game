# background.py - Expanded with multiple layers and effects
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STAR_SPEED, COLOR_BLACK, COLOR_WHITE

class Background:
    """
    Base scrolling background.
    """
    def __init__(self):
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2))
        self.image.fill(COLOR_BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = -SCREEN_HEIGHT
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 0:
            self.rect.y = -SCREEN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, (0, self.rect.y + SCREEN_HEIGHT))

class StarField(Background):
    """
    Star field layer.
    """
    def __init__(self):
        super().__init__()
        self.stars = []
        for _ in range(300):  # More stars
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT * 2)
            size = random.randint(1, 4)
            speed = STAR_SPEED * size / 2
            self.stars.append((x, y, size, speed))

    def update(self):
        for i in range(len(self.stars)):
            x, y, size, speed = self.stars[i]
            y += speed
            if y > SCREEN_HEIGHT * 2:
                y = 0
                x = random.randint(0, SCREEN_WIDTH)
            self.stars[i] = (x, y, size, speed)

    def draw(self, screen):
        for x, y, size, _ in self.stars:
            pygame.draw.circle(screen, COLOR_WHITE, (x, int(y) % SCREEN_HEIGHT), size)
            pygame.draw.circle(screen, COLOR_WHITE, (x, int(y - SCREEN_HEIGHT) % SCREEN_HEIGHT), size)

class NebulaBackground(Background):
    """
    Nebula cloud layer.
    """
    def __init__(self):
        super().__init__()
        self.speed = 0.5
        # Generate nebula images placeholder

class PlanetBackground(Background):
    """
    Planetary bodies layer.
    """
    def __init__(self):
        super().__init__()
        self.speed = 0.2
        # Generate planets placeholder
