# 🐍 Nokia Snake

A classic Nokia-style Snake game built with Python and Pygame, recreated with modern code structure and smooth graphics.

## Features

- 🎮 Smooth snake movement with directional sprite graphics
- 🍎 Randomised fruit that never spawns on the snake
- 🔊 Crunch sound on eating
- 🏆 In-session high-score tracking
- 📺 Start screen & game-over overlay
- ♟️ Chequerboard grass background

## Project Structure

```
Snake-game/
├── assets/
│   ├── fonts/          # PoetsenOne-Regular.ttf
│   ├── graphics/       # Snake sprites + apple
│   └── sounds/         # crunch.wav
├── snake_game/         # Python package
│   ├── settings.py     # Constants & asset paths
│   ├── fruit.py        # Fruit class
│   ├── snake.py        # Snake class
│   └── game.py         # Game loop & state machine
├── main.py             # Entry point
├── requirements.txt
└── .gitignore
```

## Setup

```bash
# 1. Clone
git clone https://github.com/StalinoAJ/Snake-Game-Nokia-.git
cd Snake-Game-Nokia-

# 2. Install dependency
pip install -r requirements.txt

# 3. Run
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| ↑ ↓ ← → | Steer the snake |
| Any arrow | Start game / Restart after game-over |
| Close window | Quit |

## Requirements

- Python 3.10+
- [Pygame](https://www.pygame.org/) 2.0+
