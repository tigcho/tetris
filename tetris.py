#!/usr/bin/env python3
import curses
import random
from dataclasses import dataclass
from typing import List

@dataclass
class Piece:
    shape: List[List[str]]
    x: int
    y: int
    ghost_y: int
    color: int

class TetrisGame:
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    TICK_RATE = 0.5
    SCORE_PER_LINE = 100
    LEVEL_UP_LINES = 10

    CYAN = 1    # I piece
    YELLOW = 2  # O piece
    PURPLE = 3  # T piece
    GREEN = 4   # S piece
    RED = 5     # Z piece
    BLUE = 6    # J piece
    WHITE = 7   # L piece
    GHOST = 8   # Ghost piece

    PIECES = {
        'I': {'shape': [['■', '■', '■', '■']], 'color': CYAN},
        'O': {'shape': [['■', '■'],
                       ['■', '■']], 'color': YELLOW},
        'T': {'shape': [['■', '■', '■'],
                       [' ', '■', ' ']], 'color': PURPLE},
        'S': {'shape': [[' ', '■', '■'],
                       ['■', '■', ' ']], 'color': GREEN},
        'Z': {'shape': [['■', '■', ' '],
                       [' ', '■', '■']], 'color': RED},
        'J': {'shape': [['■', ' ', ' '],
                       ['■', '■', '■']], 'color': BLUE},
        'L': {'shape': [[' ', ' ', '■'],
                       ['■', '■', '■']], 'color': WHITE}
    }

    def __init__(self):
        self.board = [[{'char': ' ', 'color': 0} for _ in range(self.BOARD_WIDTH)] 
                     for _ in range(self.BOARD_HEIGHT)]
        self.current_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.high_score = self.load_high_score()

    @staticmethod
    def setup_colors():
        curses.init_pair(TetrisGame.CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(TetrisGame.YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(TetrisGame.PURPLE, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(TetrisGame.GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(TetrisGame.RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(TetrisGame.BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(TetrisGame.WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(TetrisGame.GHOST, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def load_high_score(self) -> int:
        try:
            with open('.tetris_high_score', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        with open('.tetris_high_score', 'w') as f:
            f.write(str(max(self.score, self.high_score)))

    def spawn_piece(self):
        piece_type = random.choice(list(self.PIECES.keys()))
        piece_data = self.PIECES[piece_type]
        x = self.BOARD_WIDTH // 2 - len(piece_data['shape'][0]) // 2
        self.current_piece = Piece(piece_data['shape'], x, 0, 0, piece_data['color'])
        self.update_ghost_piece()

    def update_ghost_piece(self):
        if not self.current_piece:
            return
        original_y = self.current_piece.y
        while not self.check_collision():
            self.current_piece.y += 1
        self.current_piece.ghost_y = self.current_piece.y - 1
        self.current_piece.y = original_y

    def check_collision(self) -> bool:
        if not self.current_piece:
            return False
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell != ' ':
                    board_x = self.current_piece.x + x
                    board_y = self.current_piece.y + y
                    if (board_x < 0 or board_x >= self.BOARD_WIDTH or
                        board_y >= self.BOARD_HEIGHT or
                        (board_y >= 0 and self.board[board_y][board_x]['char'] != ' ')):
                        return True
        return False

    def rotate_piece(self):
        if not self.current_piece:
            return
        old_shape = self.current_piece.shape
        self.current_piece.shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
        if self.check_collision():
            self.current_piece.shape = old_shape
        else:
            self.update_ghost_piece()

    def move_piece(self, dx: int, dy: int) -> bool:
        if not self.current_piece:
            return False
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.check_collision():
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False
        self.update_ghost_piece()
        return True

    def hard_drop(self):
        if not self.current_piece:
            return
        while self.move_piece(0, 1):
            pass
        self.lock_piece()

    def lock_piece(self):
        if not self.current_piece:
            return
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell != ' ':
                    board_y = self.current_piece.y + y
                    if board_y < 0:
                        self.game_over = True
                        return
                    self.board[board_y][self.current_piece.x + x] = {
                        'char': '■',
                        'color': self.current_piece.color
                    }
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        lines_to_clear = []
        for y in range(self.BOARD_HEIGHT):
            if all(cell['char'] != ' ' for cell in self.board[y]):
                lines_to_clear.append(y)
        
        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [{'char': ' ', 'color': 0} for _ in range(self.BOARD_WIDTH)])
        
        cleared = len(lines_to_clear)
        if cleared > 0:
            self.lines_cleared += cleared
            self.score += self.SCORE_PER_LINE * cleared * self.level
            self.level = (self.lines_cleared // self.LEVEL_UP_LINES) + 1
