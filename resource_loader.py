# resource_loader.py - New module for loading resources
import pygame

class ResourceLoader:
    """
    Loads images, sounds, fonts.
    """
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, name, file):
        self.images[name] = pygame.image.load(file)

    def load_sound(self, name, file):
        self.sounds[name] = pygame.mixer.Sound(file)

    def load_font(self, name, size):
        self.fonts[name] = pygame.font.Font(None, size)

    def load_all_images(self):
        # Placeholder for loading all
        pass

    def load_all_sounds(self):
        # Placeholder
        pass
