# input_handler.py - New module for input
from pygame.locals import *

class InputHandler:
    """
    Centralized input handling.
    """
    def __init__(self):
        self.keys = pygame.key.get_pressed()
        self.events = []

    def handle_events(self):
        self.events = pygame.event.get()
        self.keys = pygame.key.get_pressed()
        for event in self.events:
            if event.type == QUIT:
                # Handle quit
                pass

    def get_keys(self):
        return self.keys

    def is_key_pressed(self, key):
        return self.keys[key]

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
