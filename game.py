# Step 2: Create Tetris Board

import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

TETROMINOS = {
    'I': [(0, 0), (1, 0), (2, 0), (3, 0)],
    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'T': [(0, 0), (1, 0), (2, 0), (1, 1)],
    'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
    'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
    'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
    'L': [(2, 0), (0, 1), (1, 1), (2, 1)]
}

class TetrisGame:
    def __init__(self):
        self.board = [(0) * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.highscore = self.load_highscore()
        self.curr_piece = self.get_piece()
        self.next_piece = self.get_piece()
        self.hold_piece = None
        self.held = False

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except:
            return 0

    def save_highscore(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))

    def get_piece(self):
        return {
            'type': random.choice(list(TETROMINOS.keys())),
            'rotation': 0,
            'x': BOARD_WIDTH // 2 - 2,
            'y': 0
        }

    def rotate_piece(self):
        cx, cy = piece['coords'][0]
        new_coords = []
        for x, y in piece['coords']:
            new_x = cx - (y - cy)
            new_y = cy + (x - cx)
            new_coords.append((new_x, new_y))
        piece['coords'] = new_coords
