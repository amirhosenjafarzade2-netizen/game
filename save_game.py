# save_game.py - Expanded saving with more data
import json
import os

class SaveGame:
    """
    Handles saving and loading game state.
    """
    def __init__(self, file='save.json'):
        self.file = file

    def save(self, data):
        with open(self.file, 'w') as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                return json.load(f)
        return None

    def delete_save(self):
        if os.path.exists(self.file):
            os.remove(self.file)
