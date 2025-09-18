# ai.py - Expanded AI behaviors
import random
from constants import AI_AGGRESSION_LOW, AI_AGGRESSION_HIGH

class EnemyAI:
    """
    Base AI for enemies.
    """
    def __init__(self, enemy):
        self.enemy = enemy
        self.aggression = random.uniform(AI_AGGRESSION_LOW, AI_AGGRESSION_HIGH)

    def update(self, player, enemy_bullets):
        # Base behavior
        pass

class BasicAI(EnemyAI):
    pass

class AggressiveAI(EnemyAI):
    def update(self, player, enemy_bullets):
        # Move towards player
        if player.rect.x > self.enemy.rect.x:
            self.enemy.rect.x += self.enemy.speed * 0.5 * self.aggression
        elif player.rect.x < self.enemy.rect.x:
            self.enemy.rect.x -= self.enemy.speed * 0.5 * self.aggression

class DefensiveAI(EnemyAI):
    def update(self, player, enemy_bullets):
        # Avoid player
        if player.rect.x > self.enemy.rect.x:
            self.enemy.rect.x -= self.enemy.speed * 0.3
        elif player.rect.x < self.enemy.rect.x:
            self.enemy.rect.x += self.enemy.speed * 0.3

class SwarmAI(EnemyAI):
    def __init__(self, enemy, swarm_group):
        super().__init__(enemy)
        self.swarm_group = swarm_group

    def update(self, player, enemy_bullets):
        # Swarm behavior placeholder
        pass

class BossAI(EnemyAI):
    def update(self, player, enemy_bullets):
        # Complex boss behaviors
        pass
