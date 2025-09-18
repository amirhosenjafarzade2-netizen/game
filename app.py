# main.py - Main entry point for Epic Space Shooter with Streamlit integration
"""
Main entry point for Epic Space Shooter, a Pygame-based shoot-em-up game.
Initializes game components, manages game states, and integrates with Streamlit via config.json.
Handles saved game loading and stats tracking for web display.
"""
import pygame
from pygame.locals import *
import json
import sys
import os
import logging
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

# Configure logging
logging.basicConfig(filename='game.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Verify dependencies
try:
    import pygame
    import numpy
except ImportError as e:
    logger.error("Missing dependency: %s", e)
    print(f"Error: Missing dependency {e}. Please run 'pip install -r requirements.txt'.")
    sys.exit(1)

# Initialize Pygame
try:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Epic Space Shooter - Ultimate Shmup Edition")
    clock = pygame.time.Clock()
except Exception as e:
    logger.error("Pygame initialization failed: %s", e)
    print(f"Error initializing Pygame: {e}")
    sys.exit(1)

# Initialize game objects and managers
"""
Initialize all core components: player, enemies, UI, and managers for collisions, particles, etc.
Each component is critical for gameplay functionality.
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
multiplayer_manager = MultiplayerManager()
screen_effects = ScreenEffects(screen)
input_handler = InputHandler()
collision_manager = CollisionManager()
resource_loader = ResourceLoader()

# Load resources
"""
Load images, sounds, and fonts to ensure all assets are available.
Log any failures for debugging.
"""
try:
    resource_loader.load_all_images()
    resource_loader.load_all_sounds()
    resource_loader.load_font("default", 36)
    resource_loader.load_font("small", 24)
    logger.info("Resources loaded successfully")
except Exception as e:
    logger.error("Resource loading failed: %s", e)
    print(f"Error loading resources: {e}")
    sys.exit(1)

# Load configuration from Streamlit
"""
Read config.json generated by app.py to set difficulty and audio volumes.
Fall back to defaults if file is missing or invalid.
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
        logger.info("Loaded config: difficulty=%s, sound_volume=%.2f, music_volume=%.2f",
                    config.difficulty, config.sound_volume, config.music_volume)
    except json.JSONDecodeError as e:
        logger.error("Invalid config.json format: %s", e)
    except Exception as e:
        logger.error("Error loading config: %s", e)

# Game variables
"""
Set up game state, difficulty, and counters.
Check for --load flag to start with saved game data.
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
multiplayer_mode = False

# Save stats for Streamlit display
def save_stats():
    """
    Save game statistics to stats.json for Streamlit display.
    """
    stats = {
        "kills": player_stats.kills,
        "powerups": player_stats.powerups_collected,
        "bosses": achievements.counters.get("bosses", 0)
    }
    try:
        with open("stats.json", "w") as f:
            json.dump(stats, f)
        logger.info("Saved game stats")
    except Exception as e:
        logger.error("Error saving stats: %s", e)

# Main game loop
"""
Core game loop handling all states: menu, settings, highscores, playing, game over.
Updates entities, processes input, and renders at 60 FPS.
"""
while running:
    input_handler.handle_events()

    if game_state == "menu":
        """
        Display main menu and handle user selections for starting, loading, or quitting.
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
            logger.info("Started new game")
        elif action == "load" or load_game:
            save_data = save_game.load()
            if save_data:
                player.load_from_save(save_data['player'])
                level_manager.level = save_data['level']
                score_system.score = save_data['score']
                current_level = level_manager.level
                game_state = "playing"
                load_game = False
                music_manager.play_background_music(f"level{current_level}")
                logger.info("Loaded saved game: level=%d, score=%d", current_level, score_system.score)
            else:
                logger.warning("No save file found")
        elif action == "settings":
            game_state = "settings"
        elif action == "highscores":
            game_state = "highscores"
        elif action == "quit":
            running = False
            logger.info("Game quit from menu")
        pygame.display.flip()

    elif game_state == "settings":
        """
        Allow configuration of game settings like difficulty and audio.
        """
        settings_menu.draw(screen)
        settings_action = settings_menu.handle_selection(input_handler.get_keys())
        if settings_action == "back":
            game_state = "menu"
        elif settings_action == "difficulty":
            config.set_difficulty(settings_menu.get_selected_difficulty())
            difficulty = config.get_difficulty()
            logger.info("Difficulty set to %s", config.difficulty)
        elif settings_action == "sound_volume":
            config.sound_volume = settings_menu.get_selected_volume()
            sound_manager.set_volume(config.sound_volume)
            logger.info("Sound volume set to %.2f", config.sound_volume)
        elif settings_action == "music_volume":
            config.music_volume = settings_menu.get_selected_volume()
            music_manager.set_volume(config.music_volume)
            logger.info("Music volume set to %.2f", config.music_volume)
        pygame.display.flip()

    elif game_state == "highscores":
        """
        Display top 10 high scores and return to menu on escape.
        """
        highscore_menu.draw(screen, highscore.get_top_scores())
        if input_handler.is_key_pressed(K_ESCAPE):
            game_state = "menu"
            logger.info("Returned to menu from highscores")
        pygame.display.flip()

    elif game_state == "playing":
        """
        Core gameplay: update entities, handle collisions, and render.
        Supports pausing and saving game state.
        """
        if paused:
            pause_menu.draw(screen)
            pause_action = pause_menu.handle_selection(input_handler.get_keys())
            if pause_action == "resume":
                paused = False
                logger.info("Game resumed")
            elif pause_action == "save":
                save_data = {
                    'player': player.save_data(),
                    'level': level_manager.level,
                    'score': score_system.score
                }
                save_game.save(save_data)
                logger.info("Game saved")
            elif pause_action == "settings":
                game_state = "settings"
            elif pause_action == "quit":
                game_state = "menu"
                music_manager.stop_music()
                save_stats()
                logger.info("Quit to menu from pause")
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
            level_design = {
                1: Level1Design, 2: Level2Design, 3: Level3Design, 4: Level4Design,
                5: Level5Design, 6: Level6Design, 7: Level7Design
            }.get(current_level, Level1Design)(current_level)
            for enemy in level_design.get_wave(wave_count % MAX_WAVES_PER_LEVEL):
                enemy_ai.apply_ai(enemy, current_level)
                enemies.add(enemy)
            logger.info("Spawned wave %d in level %d", wave_count, current_level)

        if level_manager.should_spawn_powerup():
            powerup = level_design.get_powerup()
            powerups.add(powerup)
            logger.info("Spawned powerup")

        if wave_manager.is_mini_boss_wave(wave_count):
            mini_boss = MiniBoss(current_level)
            boss_ai.apply_ai(mini_boss)
            enemies.add(mini_boss)
            logger.info("Spawned mini-boss")

        if level_manager.is_boss_time() and not boss_active:
            if current_level == MAX_LEVEL:
                boss = FinalBoss()
            else:
                boss = PhaseBoss(current_level)
            boss_ai.apply_ai(boss)
            enemies.add(boss)
            boss_active = True
            music_manager.play_background_music("boss")
            logger.info("Spawned boss for level %d", current_level)

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
            save_stats()
            logger.info("Game over - Score: %d", score_system.score)

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
        Display game over screen with score and high score.
        Allow restarting to menu.
        """
        screen_effects.apply_shake()
        ui.draw_game_over(screen, score_system.score, highscore)
        if input_handler.is_key_pressed(K_r):
            game_state = "menu"
            music_manager.stop_music()
            save_stats()
            logger.info("Returned to menu from game over")
        pygame.display.flip()

# Cleanup
"""
Clean up resources and save final stats before exiting.
"""
pygame.quit()
logging_system.close()
if os.path.exists("config.json"):
    os.remove("config.json")
save_stats()
logger.info("Game terminated")
