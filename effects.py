# effects.py - New module for screen effects
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class ScreenEffects:
    """
    Manages screen effects like shake, fade.
    """
    def __init__(self, screen):
        self.screen = screen
        self.shake_duration = 0
        self.shake_intensity = 0
        self.fade_alpha = 0
        self.fade_speed = 0

    def apply_shake(self, duration=20, intensity=5):
        self.shake_duration = duration
        self.shake_intensity = intensity

    def apply_fade_out(self, speed=5):
        self.fade_alpha = 0
        self.fade_speed = speed

    def apply_effects(self):
        if self.shake_duration > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            # Apply offset placeholder
            self.shake_duration -= 1

        if self.fade_speed > 0:
            self.fade_alpha += self.fade_speed
            if self.fade_alpha > 255:
                self.fade_alpha = 255
                self.fade_speed = 0
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surf, (0, 0))

class ShakeEffect(ScreenEffects):
    pass

class FadeEffect(ScreenEffects):
    pass

class TrailEffect:
    def __init__(self, obj):
        self.obj = obj
        self.trail = []

    def update(self):
        self.trail.append((self.obj.rect.centerx, self.obj.rect.centery))
        if len(self.trail) > 10:
            self.trail.pop(0)

    def draw(self, screen):
        for i, pos in enumerate(self.trail):
            alpha = 255 * (i / len(self.trail))
            surf = pygame.Surface((10, 10))
            surf.set_alpha(alpha)
            surf.fill(COLOR_WHITE)
            screen.blit(surf, pos)
