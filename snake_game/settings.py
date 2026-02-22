"""
settings.py — All game-wide constants and asset path helpers.
"""

from pathlib import Path

# ── Base paths ──────────────────────────────────────────────────
# All paths are resolved relative to this file so the game can be
# launched from any working directory.
ASSETS_DIR  = Path(__file__).parent.parent / "assets"
GRAPHICS    = ASSETS_DIR / "graphics"
SOUNDS      = ASSETS_DIR / "sounds"
FONTS       = ASSETS_DIR / "fonts"

# ── Grid ────────────────────────────────────────────────────────
CELL_SIZE   = 40        # pixels per grid cell
CELL_NUMBER = 19        # grid is CELL_NUMBER × CELL_NUMBER

# ── Timing ──────────────────────────────────────────────────────
FPS             = 60
GAME_SPEED_MS   = 150   # milliseconds between snake moves

# ── Colours ─────────────────────────────────────────────────────
COLOR_BG            = (175, 215, 70)    # light green background
COLOR_GRASS         = (167, 209, 61)    # darker grass cell
COLOR_SCORE_TEXT    = (56,  74,  12)    # dark green text
COLOR_OVERLAY       = (0, 0, 0, 160)    # semi-transparent black
COLOR_WHITE         = (255, 255, 255)
COLOR_TITLE         = (56, 74, 12)

# ── Window ──────────────────────────────────────────────────────
WINDOW_SIZE  = (CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE)
WINDOW_TITLE = "Nokia Snake"

# ── Font size ───────────────────────────────────────────────────
FONT_SIZE_SCORE     = 25
FONT_SIZE_UI        = 36
FONT_SIZE_UI_SMALL  = 22
