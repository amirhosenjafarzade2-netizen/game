# particle.py - Expanded particle system with more types
import pygame
import random
from constants import PARTICLE_LIFETIME, EXPLOSION_PARTICLES, COLOR_RED, COLOR_YELLOW, COLOR_GRAY, COLOR_WHITE

class Particle(pygame.sprite.Sprite):
    """
    Base particle.
    """
    def __init__(self, x, y, color, vel_range=3, lifetime=PARTICLE_LIFETIME, size=5):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = random.uniform(-vel_range, vel_range)
        self.vel_y = random.uniform(-vel_range, vel_range)
        self.lifetime = lifetime
        self.alpha = 255
        self.fade_rate = 5

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.lifetime -= 1
        self.alpha = max(0, self.alpha - self.fade_rate)
        self.image.set_alpha(self.alpha)
        if self.lifetime <= 0:
            self.kill()

class SmokeParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_GRAY, vel_range=1, lifetime=60, size=10)
        self.fade_rate = 3

class FireParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_RED, vel_range=4, lifetime=25, size=8)

class SparkParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_YELLOW, vel_range=5, lifetime=15, size=3)

class DebrisParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_GRAY, vel_range=2, lifetime=40, size=6)

class GlowParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_WHITE, vel_range=0.5, lifetime=50, size=4)
        self.fade_rate = 2

class ParticleSystem(pygame.sprite.Group):
    def add_explosion(self, pos):
        for _ in range(EXPLOSION_PARTICLES):
            particle = random.choice([FireParticle, SparkParticle])(*pos)
            self.add(particle)
        for _ in range(15):
            particle = SmokeParticle(*pos)
            self.add(particle)

    def add_impact(self, pos):
        for _ in range(10):
            particle = SparkParticle(*pos)
            self.add(particle)

    def add_trail(self, pos):
        for _ in range(5):
            particle = GlowParticle(*pos)
            self.add(particle)

    # Add more effects
