# sound_manager.py - Expanded with music and more sounds
import pygame
from constants import SOUND_VOLUME_MAX, MUSIC_VOLUME_MAX

class SoundManager:
    """
    Manages sound effects.
    """
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.volume = SOUND_VOLUME_MAX

    def load_sound(self, name, file):
        self.sounds[name] = pygame.mixer.Sound(file)

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].set_volume(self.volume)
            self.sounds[name].play()

    def set_volume(self, vol):
        self.volume = vol

class MusicManager(SoundManager):
    """
    Manages background music.
    """
    def __init__(self):
        super().__init__()
        self.current_track = None
        self.volume = MUSIC_VOLUME_MAX

    def play_background_music(self, track):
        if self.current_track != track:
            pygame.mixer.music.load(track + '.mp3')
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.current_track = track

    def stop_music(self):
        pygame.mixer.music.stop()
