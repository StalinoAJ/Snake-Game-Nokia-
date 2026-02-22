"""
snake.py — Snake class.
"""

import pygame
from pygame.math import Vector2

from snake_game.settings import CELL_SIZE, GRAPHICS, SOUNDS


class Snake:
    """The player-controlled snake."""

    def __init__(self) -> None:
        self.body: list[Vector2] = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction: Vector2 = Vector2(1, 0)
        self.new_block: bool = False

        # ── Graphics ───────────────────────────────────────────────── #
        g = str(GRAPHICS) + "/"
        self.head_up    = pygame.image.load(g + "head_up.png").convert_alpha()
        self.head_down  = pygame.image.load(g + "head_down.png").convert_alpha()
        self.head_right = pygame.image.load(g + "head_right.png").convert_alpha()
        self.head_left  = pygame.image.load(g + "head_left.png").convert_alpha()

        self.tail_up    = pygame.image.load(g + "tail_up.png").convert_alpha()
        self.tail_down  = pygame.image.load(g + "tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load(g + "tail_right.png").convert_alpha()
        self.tail_left  = pygame.image.load(g + "tail_left.png").convert_alpha()

        self.body_vertical   = pygame.image.load(g + "body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load(g + "body_horizontal.png").convert_alpha()

        self.body_tr = pygame.image.load(g + "body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load(g + "body_tl.png").convert_alpha()
        self.body_br = pygame.image.load(g + "body_br.png").convert_alpha()
        self.body_bl = pygame.image.load(g + "body_bl.png").convert_alpha()

        # ── Sound ──────────────────────────────────────────────────── #
        self.crunch_sound = pygame.mixer.Sound(str(SOUNDS / "crunch.wav"))

        # Resolved head / tail images (updated each frame)
        self.head: pygame.Surface = self.head_right
        self.tail: pygame.Surface = self.tail_left

    # ------------------------------------------------------------------ #

    def reset(self) -> None:
        """Return snake to its initial three-block state."""
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)   # bug-fix: also reset direction
        self.new_block = False

    # ── Movement ───────────────────────────────────────────────────── #

    def move(self) -> None:
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self) -> None:
        self.new_block = True

    # ── Graphics ───────────────────────────────────────────────────── #

    def _update_head_graphic(self) -> None:
        relation = self.body[1] - self.body[0]
        if relation == Vector2(1, 0):
            self.head = self.head_left
        elif relation == Vector2(-1, 0):
            self.head = self.head_right
        elif relation == Vector2(0, 1):
            self.head = self.head_up
        elif relation == Vector2(0, -1):
            self.head = self.head_down

    def _update_tail_graphic(self) -> None:
        relation = self.body[-2] - self.body[-1]
        if relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif relation == Vector2(0, -1):
            self.tail = self.tail_down

    def draw(self, surface: pygame.Surface) -> None:
        self._update_head_graphic()
        self._update_tail_graphic()

        for index, block in enumerate(self.body):
            x = int(block.x * CELL_SIZE)
            y = int(block.y * CELL_SIZE)
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if index == 0:
                surface.blit(self.head, rect)
            elif index == len(self.body) - 1:
                surface.blit(self.tail, rect)
            else:
                prev = self.body[index + 1] - block
                nxt  = self.body[index - 1] - block
                if prev.x == nxt.x:
                    surface.blit(self.body_vertical, rect)
                elif prev.y == nxt.y:
                    surface.blit(self.body_horizontal, rect)
                else:
                    if (prev.x == -1 and nxt.y == -1) or (prev.y == -1 and nxt.x == -1):
                        surface.blit(self.body_tl, rect)
                    elif (prev.x == -1 and nxt.y == 1) or (prev.y == 1 and nxt.x == -1):
                        surface.blit(self.body_bl, rect)
                    elif (prev.x == 1 and nxt.y == -1) or (prev.y == -1 and nxt.x == 1):
                        surface.blit(self.body_tr, rect)
                    elif (prev.x == 1 and nxt.y == 1) or (prev.y == 1 and nxt.x == 1):
                        surface.blit(self.body_br, rect)

    # ── Sound ──────────────────────────────────────────────────────── #

    def play_crunch_sound(self) -> None:
        self.crunch_sound.play()

    # ── Properties ─────────────────────────────────────────────────── #

    @property
    def score(self) -> int:
        """Current score = number of fruits eaten."""
        return len(self.body) - 3
