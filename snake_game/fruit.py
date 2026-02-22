"""
fruit.py — Fruit (food) class.
"""

import random
import pygame
from pygame.math import Vector2

from snake_game.settings import CELL_NUMBER, CELL_SIZE, GRAPHICS


class Fruit:
    """A single food item placed randomly on the grid."""

    def __init__(self, occupied: list[Vector2] | None = None) -> None:
        self.image = pygame.image.load(str(GRAPHICS / "apple.png")).convert_alpha()
        self.pos = Vector2(0, 0)
        self.randomize(occupied=occupied)

    # ------------------------------------------------------------------ #

    def randomize(self, occupied: list[Vector2] | None = None) -> None:
        """Place the fruit at a random empty cell.

        Args:
            occupied: List of grid positions already taken by the snake.
                      If provided, the fruit will never spawn on those cells.
        """
        occupied_set = set((int(v.x), int(v.y)) for v in occupied) if occupied else set()

        while True:
            x = random.randint(0, CELL_NUMBER - 1)
            y = random.randint(0, CELL_NUMBER - 1)
            if (x, y) not in occupied_set:
                self.pos = Vector2(x, y)
                break

    def draw(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(
            int(self.pos.x * CELL_SIZE),
            int(self.pos.y * CELL_SIZE),
            CELL_SIZE,
            CELL_SIZE,
        )
        surface.blit(self.image, rect)
