# main.py - Main entry point for Epic Space Shooter with Streamlit integration
"""
This module serves as the main entry point for the Epic Space Shooter game.
It initializes Pygame, manages game states, and handles core game loop logic.
Integrates with Streamlit via config.json and --load flag for saved games.
"""
import pygame
from pygame.locals import *
import json
import sys
import os
from player import Player, PlayerControls, PlayerStats
from enemy import (
    Enemy, KamikazeEnemy, ShooterEnemy, ZigZagEnemy, BomberEnemy, StealthEnemy,
    SwarmerEnemy, TankEnemy, SniperEnemy, TeleporterEnemy, HealerEnemy, DroneEnemy,
    MissileEnemy, LaserEnemy, ShieldedEnemy, ExplosiveEnemy
)
from bullet import (
    Bullet, PlayerBullet, EnemyBullet, HomingBullet, LaserBullet,
    SpreadBullet, PiercingBullet, ExplosiveBullet, SlowBullet, FastBullet
)
from ui import UI, HUD, MiniMap, ScoreBoard
from levels import LevelManager, LevelDesigner, WaveManager
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SPEED, ENEMY_SPEED, BULLET_SPEED,
    POWERUP_SPEED, PARTICLE_LIFETIME, EXPLOSION_PARTICLES, BOSS_HEALTH,
    MINI_BOSS_HEALTH, PLAYER_HEALTH, SHIELD_DURATION, SPEED_BOOST_DURATION,
    WEAPON_UPGRADE_DURATION, DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD,
    STAR_SPEED, GRAVITY, MAX_LEVEL, SCORE_MULTIPLIER
)
from menu import Menu, PauseMenu, SettingsMenu, HighScoreMenu
from highscore import HighScore
from sound_manager import SoundManager, MusicManager
from powerup import (
    PowerUp, ShieldPowerUp, SpeedPowerUp, WeaponPowerUp, LifePowerUp,
    ScorePowerUp, InvincibilityPowerUp, MagnetPowerUp, BombPowerUp
)
from boss import Boss, MiniBoss, PhaseBoss, FinalBoss
from background import Background, StarField, NebulaBackground, PlanetBackground
from particle import (
    ParticleSystem, SmokeParticle, FireParticle, SparkParticle,
    DebrisParticle, GlowParticle
)
from animation import AnimationManager, PlayerAnimation, EnemyAnimation, BulletAnimation
from ai import EnemyAI, SwarmAI, BossAI
from score_system import ScoreSystem
from config import Config
from save_game import SaveGame
from achievements import AchievementSystem
from logging_system import LoggingSystem
from multiplayer import MultiplayerManager
from effects import ScreenEffects, ShakeEffect, FadeEffect
from input_handler import InputHandler
from collision_manager import CollisionManager
from resource_loader import ResourceLoader
from level_designs import Level1Design, Level2Design, Level3Design, Level4Design, Level5Design, Level6Design, Level7Design

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Epic Space Shooter - Ultimate Shmup Edition")
clock = pygame.time.Clock()

# Initialize all game objects and managers
"""
Initialize core game components, including player, enemies, UI, and managers.
Each manager handles a specific aspect of the game (e.g., collisions, particles).
"""
player = Player()
player_controls = PlayerControls(player)
player_stats = PlayerStats(player)
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
particles = ParticleSystem()
ui = UI()
hud = HUD()
mini_map = MiniMap()
score_board = ScoreBoard()
level_manager = LevelManager()
level_designer = LevelDesigner()
wave_manager = WaveManager()
menu = Menu(screen)
pause_menu = PauseMenu(screen)
settings_menu = SettingsMenu(screen)
highscore_menu = HighScoreMenu(screen)
highscore = HighScore()
sound_manager = SoundManager()
music_manager = MusicManager()
background = Background()
star_field = StarField()
nebula_background = NebulaBackground()
planet_background = PlanetBackground()
animation_manager = AnimationManager()
enemy_ai = EnemyAI()
swarm_ai = SwarmAI()
boss_ai = BossAI()
score_system = ScoreSystem()
config = Config()
save_game = SaveGame()
achievements = AchievementSystem()
logging_system = LoggingSystem()
multiplayer_manager = MultiplayerManager()  # Placeholder for future multiplayer
screen_effects = ScreenEffects(screen)
input_handler = InputHandler()
collision_manager = CollisionManager()
resource_loader = ResourceLoader()

# Load resources
"""
Load all game assets (images, sounds, fonts) using the resource loader.
This ensures all assets are available before the game starts.
"""
resource_loader.load_all_images()
resource_loader.load_all_sounds()
resource_loader.load_font("default", 36)
resource_loader.load_font("small", 24)

# Load configuration from Streamlit
"""
Read configuration settings from config.json if it exists.
This allows Streamlit (app.py) to set difficulty and audio volumes.
"""
if os.path.exists("config.json"):
    try:
        with open("config.json", "r") as f:
            config_data = json.load(f)
            config.set_difficulty(config_data.get("difficulty", "normal"))
            config.sound_volume = config_data.get("sound_volume", 1.0)
            config.music_volume = config_data.get("music_volume", 0.8)
        sound_manager.set_volume(config.sound_volume)
        music_manager.set_volume(config.music_volume)
    except json.JSONDecodeError:
        logging_system.log_event("Error: Invalid config.json format")
    except Exception as e:
        logging_system.log_event(f"Error loading config: {e}")

# Game variables
"""
Initialize core game variables, including state, difficulty, and counters.
Check for --load flag to start in playing state with saved data.
"""
game_state = "menu"
load_game = "--load" in sys.argv
if load_game:
    game_state = "playing"
running = True
paused = False
difficulty = config.get_difficulty()
current_level = 1
wave_count = 0
boss_active = False
multiplayer_mode = False  # Placeholder for future multiplayer

# Main game loop
"""
The main game loop handles all game states: menu, settings, highscores, playing, and game over.
Processes input, updates game objects, and renders the scene at 60 FPS.
"""
while running:
    input_handler.handle_events()  # Centralized input handling

    if game_state == "menu":
        """
        Menu state: Display main menu and handle user selections.
        Supports starting a new game, loading a saved game, settings, high scores, or quitting.
        """
        menu.draw(screen)
        action = menu.handle_selection(input_handler.get_keys())
        if action == "start":
            game_state = "playing"
            player.reset()
            enemies.empty()
            player_bullets.empty()
            enemy_bullets.empty()
            powerups.empty()
            level_manager.reset()
            score_system.reset()
            achievements.reset()
            wave_count = 0
            boss_active = False
            music_manager.play_background_music("level1")
            logging_system.log_event("New game started")
        elif action == "load" or load_game:
            save_data = save_game.load()
            if save_data:
                player.load_from_save(save_data['player'])
                level_manager.level = save_data['level']
                score_system.score = save_data['score']
                current_level = level_manager.level
                game_state = "playing"
                load_game = False  # Reset flag after loading
                music_manager.play_background_music(f"level{current_level}")
                logging_system.log_event("Loaded saved game")
            else:
                logging_system.log_event("No save file found")
        elif action == "settings":
            game_state = "settings"
        elif action == "highscores":
            game_state = "highscores"
        elif action == "quit":
            running = False
            logging_system.log_event("Game quit from menu")
        pygame.display.flip()

    elif game_state == "settings":
        """
        Settings state: Allow configuration of difficulty, audio, and controls.
        Updates config object and saves changes.
        """
        settings_menu.draw(screen)
        settings_action = settings_menu.handle_selection(input_handler.get_keys())
        if settings_action == "back":
            game_state = "menu"
        elif settings_action == "difficulty":
            config.set_difficulty(settings_menu.get_selected_difficulty())
            difficulty = config.get_difficulty()
            logging_system.log_event(f"Difficulty set to {config.difficulty}")
        elif settings_action == "sound_volume":
            config.sound_volume = settings_menu.get_selected_volume()
            sound_manager.set_volume(config.sound_volume)
        elif settings_action == "music_volume":
            config.music_volume = settings_menu.get_selected_volume()
            music_manager.set_volume(config.music_volume)
        pygame.display.flip()

    elif game_state == "highscores":
        """
        Highscores state: Display top scores and allow returning to menu.
        """
        highscore_menu.draw(screen, highscore.get_top_scores())
        if input_handler.is_key_pressed(K_ESCAPE):
            game_state = "menu"
            logging_system.log_event("Returned to menu from highscores")
        pygame.display.flip()

    elif game_state == "playing":
        """
        Playing state: Core game loop with updates, collisions, and rendering.
        Handles pausing, entity updates, and level progression.
        """
        if paused:
            pause_menu.draw(screen)
            pause_action = pause_menu.handle_selection(input_handler.get_keys())
            if pause_action == "resume":
                paused = False
                logging_system.log_event("Game resumed")
            elif pause_action == "save":
                save_data = {
                    'player': player.save_data(),
                    'level': level_manager.level,
                    'score': score_system.score
                }
                save_game.save(save_data)
                logging_system.log_event("Game saved")
            elif pause_action == "settings":
                game_state = "settings"
            elif pause_action == "quit":
                game_state = "menu"
                music_manager.stop_music()
                logging_system.log_event("Quit to menu from pause")
            pygame.display.flip()
            continue

        # Update player
        player_controls.update(input_handler.get_keys(), difficulty)
        player_stats.update()

        # Level and wave management
        level_manager.update()
        wave_manager.update()
        current_level = level_manager.level

        # Spawn entities
        if wave_manager.should_spawn_wave():
            wave_count += 1
            # Use level-specific designs
            level_design = {
                1: Level1Design,
                2: Level2Design,
                3: Level3Design,
                4: Level4Design,
                5: Level5Design,
                6: Level6Design,
                7: Level7Design
                # Add more levels up to MAX_LEVEL
            }.get(current_level, Level1Design)(current_level)
            for enemy in level_design.get_wave(wave_count % MAX_WAVES_PER_LEVEL):
                enemy_ai.apply_ai(enemy, current_level)
                enemies.add(enemy)
            logging_system.log_event(f"Spawned wave {wave_count} in level {current_level}")

        if level_manager.should_spawn_powerup():
            powerup = level_design.get_powerup()
            powerups.add(powerup)
            logging_system.log_event("Spawned powerup")

        if wave_manager.is_mini_boss_wave(wave_count):
            mini_boss = MiniBoss(current_level)
            boss_ai.apply_ai(mini_boss)
            enemies.add(mini_boss)
            logging_system.log_event("Spawned mini-boss")

        if level_manager.is_boss_time() and not boss_active:
            if current_level == MAX_LEVEL:
                boss = FinalBoss()
            else:
                boss = PhaseBoss(current_level)
            boss_ai.apply_ai(boss)
            enemies.add(boss)
            boss_active = True
            music_manager.play_background_music("boss")
            logging_system.log_event(f"Spawned boss for level {current_level}")

        # Update entities
        enemies.update(enemy_bullets, player, difficulty, screen_effects)
        player_bullets.update()
        enemy_bullets.update()
        powerups.update()
        particles.update()
        star_field.update()
        nebula_background.update()
        planet_background.update()
        animation_manager.update()
        score_system.update()

        # Collision handling
        collision_manager.handle_player_enemies(player, enemies, particles, sound_manager, score_system, achievements)
        collision_manager.handle_bullets_enemies(player_bullets, enemies, particles, sound_manager, score_system, achievements)
        collision_manager.handle_powerups(player, powerups, sound_manager, achievements)
        collision_manager.handle_enemy_bullets(player, enemy_bullets, sound_manager)

        # Check for game over
        if player.health <= 0:
            game_state = "game_over"
            music_manager.play_sound("game_over")
            screen_effects.apply_fade_out()
            highscore.update(score_system.score)
            logging_system.log_event(f"Game over - Score: {score_system.score}")

        # Drawing
        background.draw(screen)
        star_field.draw(screen)
        nebula_background.draw(screen)
        planet_background.draw(screen)
        screen.blit(player.image, player.rect)
        enemies.draw(screen)
        player_bullets.draw(screen)
        enemy_bullets.draw(screen)
        powerups.draw(screen)
        particles.draw(screen)
        hud.draw(screen, player_stats)
        mini_map.draw(screen, player, enemies)
        score_board.draw(screen, score_system)
        ui.draw(screen, score_system.score, player.health, level_manager.level, achievements.get_unlocked())
        screen_effects.apply_effects()

        pygame.display.flip()
        clock.tick(FPS)
        logging_system.log_frame_stats(clock.get_fps())

    elif game_state == "game_over":
        """
        Game over state: Display final score and high score, allow restarting.
        Applies screen shake and fade effects for dramatic effect.
        """
        screen_effects.apply_shake()
        ui.draw_game_over(screen, score_system.score, highscore)
        if input_handler.is_key_pressed(K_r):
            game_state = "menu"
            music_manager.stop_music()
            logging_system.log_event("Returned to menu from game over")
        pygame.display.flip()

# Cleanup
"""
Clean up Pygame and logging resources on exit.
Remove temporary config file if it exists.
"""
pygame.quit()
logging_system.close()
if os.path.exists("config.json"):
    os.remove("config.json")
logging_system.log_event("Game terminated")
