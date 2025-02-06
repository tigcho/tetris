#!/usr/bin/env python3
import curses
import time
from tetris import TetrisGame

def main(stdscr):
    # Set up curses
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(1)   # Non-blocking input
    
    # Initialize game and colors
    game = TetrisGame()
    game.setup_colors()
    game.spawn_piece()
    last_fall = time.time()
    
    while not game.game_over:
        # Clear screen
        stdscr.clear()
        
        # Handle input
        try:
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_LEFT:
                game.move_piece(-1, 0)
            elif key == curses.KEY_RIGHT:
                game.move_piece(1, 0)
            elif key == curses.KEY_DOWN:
                game.move_piece(0, 1)
            elif key == curses.KEY_UP:
                game.rotate_piece()
            elif key == ord(' '):
                game.hard_drop()
        except curses.error:
            pass

        # Automatic falling
        current_time = time.time()
        if current_time - last_fall > game.TICK_RATE / game.level:
            if not game.move_piece(0, 1):
                game.lock_piece()
            last_fall = current_time

        # Draw game board
        for y in range(game.BOARD_HEIGHT):
            for x in range(game.BOARD_WIDTH):
                cell = game.board[y][x]
                if cell['char'] == ' ':
                    stdscr.addstr(y + 1, x * 2 + 1, '·')
                else:
                    stdscr.addstr(y + 1, x * 2 + 1, cell['char'], 
                                curses.color_pair(cell['color']))

        # Draw current piece
        if game.current_piece:
            # Draw ghost piece
            for y, row in enumerate(game.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell != ' ':
                        ghost_y = game.current_piece.ghost_y + y
                        ghost_x = game.current_piece.x + x
                        if 0 <= ghost_y < game.BOARD_HEIGHT and 0 <= ghost_x < game.BOARD_WIDTH:
                            stdscr.addstr(ghost_y + 1, ghost_x * 2 + 1, '□', 
                                        curses.color_pair(game.GHOST) | curses.A_DIM)

            # Draw actual piece
            for y, row in enumerate(game.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell != ' ':
                        piece_y = game.current_piece.y + y
                        piece_x = game.current_piece.x + x
                        if 0 <= piece_y < game.BOARD_HEIGHT and 0 <= piece_x < game.BOARD_WIDTH:
                            stdscr.addstr(piece_y + 1, piece_x * 2 + 1, '■',
                                        curses.color_pair(game.current_piece.color) | curses.A_BOLD)

        # Draw score and level
        stdscr.addstr(0, game.BOARD_WIDTH * 2 + 5, f"Score: {game.score}")
        stdscr.addstr(1, game.BOARD_WIDTH * 2 + 5, f"Level: {game.level}")
        stdscr.addstr(2, game.BOARD_WIDTH * 2 + 5, f"High Score: {game.high_score}")
        
        # Add color legend
        stdscr.addstr(4, game.BOARD_WIDTH * 2 + 5, "Pieces:")
        stdscr.addstr(5, game.BOARD_WIDTH * 2 + 5, "■ I", curses.color_pair(game.CYAN) | curses.A_BOLD)
        stdscr.addstr(6, game.BOARD_WIDTH * 2 + 5, "■ O", curses.color_pair(game.YELLOW) | curses.A_BOLD)
        stdscr.addstr(7, game.BOARD_WIDTH * 2 + 5, "■ T", curses.color_pair(game.PURPLE) | curses.A_BOLD)
        stdscr.addstr(8, game.BOARD_WIDTH * 2 + 5, "■ S", curses.color_pair(game.GREEN) | curses.A_BOLD)
        stdscr.addstr(9, game.BOARD_WIDTH * 2 + 5, "■ Z", curses.color_pair(game.RED) | curses.A_BOLD)
        stdscr.addstr(10, game.BOARD_WIDTH * 2 + 5, "■ J", curses.color_pair(game.BLUE) | curses.A_BOLD)
        stdscr.addstr(11, game.BOARD_WIDTH * 2 + 5, "■ L", curses.color_pair(game.WHITE) | curses.A_BOLD)
        
        # Refresh screen
        stdscr.refresh()
        
        # Small delay to prevent CPU hogging
        time.sleep(0.01)

    # Game over
    stdscr.nodelay(0)
    stdscr.addstr(game.BOARD_HEIGHT // 2, game.BOARD_WIDTH + 2, "GAME OVER!")
    stdscr.addstr(game.BOARD_HEIGHT // 2 + 1, game.BOARD_WIDTH + 2, f"Final Score: {game.score}")
    stdscr.addstr(game.BOARD_HEIGHT // 2 + 2, game.BOARD_WIDTH + 2, "Press any key to exit")
    stdscr.refresh()
    stdscr.getch()
    
    # Save high score
    game.save_high_score()

if __name__ == "__main__":
    curses.wrapper(main)
