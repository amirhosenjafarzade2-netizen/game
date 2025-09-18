# collision_manager.py - New module for collisions
import pygame.sprite

class CollisionManager:
    """
    Handles all collisions.
    """
    def handle_player_enemies(self, player, enemies, particles, sound, score, achievements):
        hits = pygame.sprite.spritecollide(player, enemies, False)
        for hit in hits:
            if not player.invincible:
                player.take_damage(hit.damage)
                sound.play('hit')
            hit.health -= player.collision_damage
            if hit.health <= 0:
                hit.kill()
                score.add_score(hit.score_value)
                particles.add_explosion(hit.rect.center)
                sound.play('explosion')
                achievements.check_achievement('enemy_kill')

    def handle_bullets_enemies(self, bullets, enemies, particles, sound, score, achievements):
        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for bullet, enemy_hits in hits.items():
            for enemy in enemy_hits:
                enemy.health -= bullet.damage
                if enemy.health <= 0:
                    enemy.kill()
                    score.add_score(enemy.score_value)
                    particles.add_explosion(enemy.rect.center)
                    sound.play('explosion')
                    achievements.check_achievement('bullet_kill')
                else:
                    particles.add_impact(enemy.rect.center)

    def handle_powerups(self, player, powerups, sound, achievements):
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in hits:
            powerup.apply(player)
            sound.play('powerup')
            achievements.check_achievement('powerup_collect')

    def handle_enemy_bullets(self, player, bullets, sound):
        hits = pygame.sprite.spritecollide(player, bullets, True)
        for bullet in hits:
            if not player.is_shielded():
                player.take_damage(bullet.damage)
                sound.play('hit')
