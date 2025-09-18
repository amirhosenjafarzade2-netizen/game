# animation.py - Expanded animations for various objects
import pygame
from constants import ANIMATION_FRAME_RATE

class AnimationManager:
    """
    Manages all animations in the game.
    """
    def __init__(self):
        self.animations = {}

    def add(self, obj, animation):
        self.animations[obj] = animation

    def update(self):
        for animation in self.animations.values():
            animation.update()

class PlayerAnimation:
    """
    Animation for player.
    """
    def __init__(self, player):
        self.player = player
        self.frames = [player.image.copy() for _ in range(5)]  # Placeholder frames
        self.current_frame = 0
        self.frame_delay = ANIMATION_FRAME_RATE
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def get_current_frame(self):
        return self.frames[self.current_frame]

class EnemyAnimation(PlayerAnimation):
    """
    Animation for enemies.
    """
    pass

class BulletAnimation(PlayerAnimation):
    """
    Animation for bullets.
    """
    pass
