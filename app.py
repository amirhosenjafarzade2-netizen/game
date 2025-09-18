# app.py - Streamlit interface for Epic Space Shooter
import streamlit as st
import subprocess
import json
import os
from highscore import HighScore
from achievements import AchievementSystem
from config import Config

# Initialize objects
highscore = HighScore()
config = Config()
achievements = AchievementSystem()

# Streamlit page configuration
st.set_page_config(page_title="Epic Space Shooter", page_icon="🚀", layout="wide")

# Title and sidebar
st.title("Epic Space Shooter - Control Panel")
st.sidebar.header("Game Options")

# Game configuration
difficulty = st.sidebar.selectbox(
    "Select Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1  # Default to Normal
)
sound_volume = st.sidebar.slider("Sound Volume", 0.0, 1.0, config.sound_volume)
music_volume = st.sidebar.slider("Music Volume", 0.0, 1.0, config.music_volume)

# Save configuration
if st.sidebar.button("Save Settings"):
    config.set_difficulty(difficulty.lower())
    config.sound_volume = sound_volume
    config.music_volume = music_volume
    st.sidebar.success("Settings saved!")

# Launch game button
if st.button("Launch Game"):
    try:
        # Save config to a temporary file for main.py to read
        with open("config.json", "w") as f:
            json.dump({
                "difficulty": difficulty.lower(),
                "sound_volume": sound_volume,
                "music_volume": music_volume
            }, f)
        # Launch the Pygame game
        subprocess.run(["python", "main.py"])
        st.success("Game launched! Check your desktop.")
    except Exception as e:
        st.error(f"Failed to launch game: {e}")

# Display high scores
st.header("High Scores")
scores = highscore.get_top_scores()
if scores:
    for i, (score, name, date) in enumerate(scores, 1):
        st.write(f"{i}. {name} - {score} (Date: {date})")
else:
    st.write("No high scores yet.")

# Display achievements
st.header("Achievements")
unlocked = achievements.get_unlocked()
if unlocked:
    for ach in unlocked:
        desc = achievements.achievements[ach]["description"]
        st.write(f"- {ach.replace('_', ' ').title()}: {desc}")
else:
    st.write("No achievements unlocked yet.")

# Load game state
st.header("Load Game")
if os.path.exists("save.json"):
    if st.button("Load Saved Game"):
        try:
            subprocess.run(["python", "main.py", "--load"])
            st.success("Loaded saved game!")
        except Exception as e:
            st.error(f"Failed to load game: {e}")
else:
    st.write("No saved game found.")

# Game instructions
st.header("How to Play")
st.markdown("""
- **Controls**:
  - Arrow Keys: Move the ship
  - Space: Shoot
  - P or Esc: Pause
  - R: Restart after game over
- **Objective**: Survive waves of enemies, collect power-ups, and defeat bosses.
- **Power-Ups**: Health, Shield, Speed, Weapon, Life, Invincibility, Score, Magnet, Bomb
- **Tips**:
  - Avoid enemy collisions and bullets.
  - Collect power-ups to enhance your ship.
  - Watch for boss phases with unique attacks.
""")
