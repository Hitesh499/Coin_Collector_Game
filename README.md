# Python Game Project

This is a simple 2D Python game built using **Pygame**. The player collects coins, avoids obstacles, and the game includes sound effects, animations, and a game-over screen.

## 🎮 Features
- Character movement in all directions
- Coin collection with score update and sound
- Randomly thrown bouncing balls (enemies)
- Timer and background music
- Game over screen with Restart and Exit options

## 🛠 How to Run

1. Install dependencies:

pip install -r requirements.txt

2. Run the Game

python simple_game.py

3. Docker Support to package game as a Docker Container

docker build -t python-game .
docker run -it python-game

