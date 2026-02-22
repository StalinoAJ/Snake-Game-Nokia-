"""
game.py — Main game class with state machine and render loop.
"""

from __future__ import annotations

import sys
import pygame
from pygame.math import Vector2

from snake_game.settings import (
    CELL_NUMBER, CELL_SIZE, COLOR_BG, COLOR_GRASS, COLOR_SCORE_TEXT,
    COLOR_WHITE, COLOR_TITLE, FONTS, FONT_SIZE_SCORE, FONT_SIZE_UI,
    FONT_SIZE_UI_SMALL, FPS, GAME_SPEED_MS, WINDOW_SIZE, WINDOW_TITLE,
)
from snake_game.snake import Snake
from snake_game.fruit import Fruit

# ── Game states ─────────────────────────────────────────────────
WAITING   = "waiting"
PLAYING   = "playing"
GAME_OVER = "game_over"


class Game:
    """Top-level game object: owns the window, clock, and run loop."""

    def __init__(self) -> None:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        font_path = str(FONTS / "PoetsenOne-Regular.ttf")
        self.score_font = pygame.font.Font(font_path, FONT_SIZE_SCORE)
        self.ui_font    = pygame.font.Font(font_path, FONT_SIZE_UI)
        self.ui_font_sm = pygame.font.Font(font_path, FONT_SIZE_UI_SMALL)

        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, GAME_SPEED_MS)

        self.high_score: int = 0
        self.state: str = WAITING
        self._new_game()

    # ------------------------------------------------------------------ #
    #  Game management
    # ------------------------------------------------------------------ #

    def _new_game(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit(occupied=self.snake.body)

    def _update(self) -> None:
        self.snake.move()
        self._check_eat()
        self._check_fail()

    # ------------------------------------------------------------------ #
    #  Collision / eating logic
    # ------------------------------------------------------------------ #

    def _check_eat(self) -> None:
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(occupied=self.snake.body)
            self.snake.add_block()
            self.snake.play_crunch_sound()

    def _check_fail(self) -> None:
        head = self.snake.body[0]
        # Wall collision
        if not (0 <= head.x < CELL_NUMBER and 0 <= head.y < CELL_NUMBER):
            self._trigger_game_over()
            return
        # Self collision
        for block in self.snake.body[1:]:
            if block == head:
                self._trigger_game_over()
                return

    def _trigger_game_over(self) -> None:
        score = self.snake.score
        if score > self.high_score:
            self.high_score = score
        self.state = GAME_OVER

    # ------------------------------------------------------------------ #
    #  Input
    # ------------------------------------------------------------------ #

    def _handle_keydown(self, key: int) -> None:
        if self.state == WAITING:
            self.state = PLAYING
            return

        if self.state == GAME_OVER:
            self._new_game()
            self.state = PLAYING
            return

        # Steer — prevent 180° reversal
        d = self.snake.direction
        if key == pygame.K_UP    and d.y != 1:
            self.snake.direction = Vector2(0, -1)
        elif key == pygame.K_DOWN  and d.y != -1:
            self.snake.direction = Vector2(0, 1)
        elif key == pygame.K_RIGHT and d.x != -1:
            self.snake.direction = Vector2(1, 0)
        elif key == pygame.K_LEFT  and d.x != 1:
            self.snake.direction = Vector2(-1, 0)

    # ------------------------------------------------------------------ #
    #  Drawing helpers
    # ------------------------------------------------------------------ #

    def _draw_grass(self) -> None:
        for row in range(CELL_NUMBER):
            for col in range(CELL_NUMBER):
                # Chequerboard: shade every other cell
                if (row + col) % 2 == 0:
                    rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, COLOR_GRASS, rect)

    def _draw_score(self) -> None:
        score = self.snake.score
        apple_img = self.fruit.image

        text_surf = self.score_font.render(str(score), True, COLOR_SCORE_TEXT)
        score_x   = CELL_NUMBER * CELL_SIZE - 60
        score_y   = CELL_NUMBER * CELL_SIZE - 40
        text_rect = text_surf.get_rect(center=(score_x, score_y))
        apple_rect = apple_img.get_rect(midright=(text_rect.left, text_rect.centery))
        bg_rect  = pygame.Rect(
            apple_rect.left, apple_rect.top,
            apple_rect.width + text_rect.width + 8, apple_rect.height,
        )
        pygame.draw.rect(self.screen, COLOR_GRASS, bg_rect)
        self.screen.blit(text_surf, text_rect)
        self.screen.blit(apple_img, apple_rect)
        pygame.draw.rect(self.screen, COLOR_SCORE_TEXT, bg_rect, 2)

    def _draw_overlay(self, lines: list[tuple[str, pygame.font.Font, tuple]]) -> None:
        """Darken the screen and render centered text lines."""
        overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        cx = WINDOW_SIZE[0] // 2
        total_h = sum(f.size(t)[1] + 12 for t, f, _ in lines)
        y = WINDOW_SIZE[1] // 2 - total_h // 2

        for text, font, color in lines:
            surf = font.render(text, True, color)
            rect = surf.get_rect(center=(cx, y + surf.get_height() // 2))
            self.screen.blit(surf, rect)
            y += surf.get_height() + 12

    def _draw_start_screen(self) -> None:
        self._draw_overlay([
            ("Nokia Snake",        self.ui_font,    COLOR_WHITE),
            ("Press an arrow key", self.ui_font_sm, (200, 230, 150)),
            ("to start",           self.ui_font_sm, (200, 230, 150)),
        ])

    def _draw_game_over_screen(self) -> None:
        score = self.snake.score
        self._draw_overlay([
            ("Game Over",                       self.ui_font,    (255, 100, 100)),
            (f"Score: {score}",                 self.ui_font_sm, COLOR_WHITE),
            (f"Best:  {self.high_score}",       self.ui_font_sm, (255, 220, 80)),
            ("Press arrow key to restart",      self.ui_font_sm, (180, 220, 180)),
        ])

    # ------------------------------------------------------------------ #
    #  Main loop
    # ------------------------------------------------------------------ #

    def run(self) -> None:
        """Start and run the game loop until the window is closed."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.SCREEN_UPDATE and self.state == PLAYING:
                    self._update()

                if event.type == pygame.KEYDOWN:
                    self._handle_keydown(event.key)

            # ── Render ── #
            self.screen.fill(COLOR_BG)
            self._draw_grass()
            self.fruit.draw(self.screen)
            self.snake.draw(self.screen)
            self._draw_score()

            if self.state == WAITING:
                self._draw_start_screen()
            elif self.state == GAME_OVER:
                self._draw_game_over_screen()

            pygame.display.update()
            self.clock.tick(FPS)
