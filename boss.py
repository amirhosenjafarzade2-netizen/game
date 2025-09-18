# boss.py - Expanded bosses with multiple phases and attacks
import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, BOSS_HEALTH, COLOR_RED
from bullet import EnemyBullet, HomingBullet, LaserBullet, SpreadBullet

class Boss(pygame.sprite.Sprite):
    """
    Base boss class with phases.
    """
    def __init__(self, level):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill(COLOR_RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = 50
        self.health = BOSS_HEALTH * level
        self.max_health = self.health
        self.shoot_delay = 500 / level
        self.last_shot = pygame.time.get_ticks()
        self.direction = 1
        self.phase = 1
        self.damage = 20
        self.score_value = 500 * level
        self.attacks = [self.basic_attack]

    def update(self, enemy_bullets, player, difficulty, effects):
        self.rect.x += ENEMY_SPEED * self.direction * difficulty
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1

        if self.health < self.max_health * 0.75 and self.phase == 1:
            self.phase = 2
            self.attacks.append(self.advanced_attack)
        if self.health < self.max_health * 0.5 and self.phase == 2:
            self.phase = 3
            self.attacks.append(self.ultimate_attack)

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            attack = random.choice(self.attacks)
            attack(enemy_bullets, player)
            self.last_shot = now

    def basic_attack(self, enemy_bullets, player):
        for i in range(3):
            bullet = EnemyBullet(self.rect.centerx + i*20 - 20, self.rect.bottom)
            enemy_bullets.add(bullet)

    def advanced_attack(self, enemy_bullets, player):
        bullet = HomingBullet(self.rect.centerx, self.rect.bottom, player)
        enemy_bullets.add(bullet)

    def ultimate_attack(self, enemy_bullets, player):
        for angle in [-30, 0, 30]:
            bullet = SpreadBullet(self.rect.centerx, self.rect.bottom, 'down', angle)
            enemy_bullets.add(bullet)

class MiniBoss(Boss):
    def __init__(self, level):
        super().__init__(level)
        self.image = pygame.Surface((60, 60))
        self.health = MINI_BOSS_HEALTH * level
        self.score_value = 200 * level

class PhaseBoss(Boss):
    def __init__(self, level):
        super().__init__(level)
        # Additional phases

class FinalBoss(Boss):
    def __init__(self):
        super().__init__(MAX_LEVEL)
        self.health *= 2
        self.attacks.append(self.laser_sweep)

    def laser_sweep(self, enemy_bullets, player):
        bullet = LaserBullet(self.rect.centerx, self.rect.bottom, 'down')
        enemy_bullets.add(bullet)
