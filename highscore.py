# highscore.py - Expanded with player names and dates
import datetime

class HighScore:
    """
    Manages high scores with names and dates.
    """
    def __init__(self):
        self.scores = []  # List of (score, name, date)

    def update(self, score, name="Player"):
        date = datetime.date.today()
        self.scores.append((score, name, date))
        self.scores.sort(reverse=True, key=lambda x: x[0])
        self.scores = self.scores[:10]

    def get_top_scores(self):
        return self.scores
