# achievements.py - Expanded with many achievements
class AchievementSystem:
    """
    Manages achievements.
    """
    def __init__(self):
        self.achievements = {
            'first_kill': {'unlocked': False, 'description': 'Kill your first enemy'},
            '10_kills': {'unlocked': False, 'description': 'Kill 10 enemies'},
            '100_kills': {'unlocked': False, 'description': 'Kill 100 enemies'},
            'powerup_master': {'unlocked': False, 'description': 'Collect 50 powerups'},
            'boss_slayer': {'unlocked': False, 'description': 'Defeat a boss'},
            'survivor': {'unlocked': False, 'description': 'Survive with 1 health'},
            'high_score': {'unlocked': False, 'description': 'Reach 10000 score'},
            # Add 20 more achievements
            'level_5': {'unlocked': False, 'description': 'Reach level 5'},
            'level_10': {'unlocked': False, 'description': 'Reach level 10'},
            'perfect_wave': {'unlocked': False, 'description': 'Clear a wave without damage'},
            # ... continue
        }
        self.counters = {
            'kills': 0,
            'powerups': 0,
            'bosses': 0
        }

    def reset(self):
        for ach in self.achievements.values():
            ach['unlocked'] = False
        for key in self.counters:
            self.counters[key] = 0

    def check_achievement(self, event):
        if event == 'enemy_kill':
            self.counters['kills'] += 1
            if self.counters['kills'] == 1:
                self.achievements['first_kill']['unlocked'] = True
            if self.counters['kills'] == 10:
                self.achievements['10_kills']['unlocked'] = True
            if self.counters['kills'] == 100:
                self.achievements['100_kills']['unlocked'] = True
        elif event == 'powerup_collect':
            self.counters['powerups'] += 1
            if self.counters['powerups'] == 50:
                self.achievements['powerup_master']['unlocked'] = True
        elif event == 'boss_kill':
            self.counters['bosses'] += 1
            if self.counters['bosses'] == 1:
                self.achievements['boss_slayer']['unlocked'] = True
        # Add checks for all achievements

    def get_unlocked(self):
        return [key for key, val in self.achievements.items() if val['unlocked']]
