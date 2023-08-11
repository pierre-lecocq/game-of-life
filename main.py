# File: main.py
# Creation: Tue Aug  8 11:02:35 2023
# Time-stamp: <2023-08-11 15:19:42>
# Copyright (C): 2023 Pierre Lecocq

import argparse
import copy
import pygame

BG_COLOR = (30, 30, 20)
STATE_DEAD = 0
STATE_ALIVE = 1
STATE_ALIVE_NEW = 2

class GameOfLife:
    """John Conway's Game of Life"""
    def __init__(self, opts):
        self.fps = opts.fps
        pygame.init()
        pygame.display.set_caption('John Conway\'s Game of Life (%dx%d@%dfps)' % (opts.columns, opts.rows, opts.fps))
        self.clock = pygame.time.Clock()
        self.grid = Grid(opts.rows, opts.columns, opts.size, opts.gap)
        self.screen = pygame.display.set_mode((self.grid.screen_width(), self.grid.screen_height()))

    def run_loop(self):
        """Run main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill(BG_COLOR)
            self.grid.apply_rules()
            self.grid.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

class Grid:
    """Grid management and drawing"""
    def __init__(self, rows, columns, size, gap):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.gap = gap
        self.board = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.init_board()

    def screen_width(self):
        """Get screen width in pixels"""
        return self.columns * self.size + (self.columns * self.gap) + 1

    def screen_height(self):
        """Get screen height in pixels"""
        return self.rows * self.size + (self.rows * self.gap) + 1

    def init_board(self):
        """Initialize board with a common shape"""
        row = (self.rows - 1) // 2
        col = (self.columns - 1) // 2
        self.init_glider(row - 8, col - 5)
        self.init_spaceship(row, col + 5)

    def init_glider(self, row, col):
        """Initialize a glider"""
        self.board[row - 1][col] = STATE_ALIVE
        self.board[row][col + 1] = STATE_ALIVE
        self.board[row + 1][col + 1] = STATE_ALIVE
        self.board[row + 1][col] = STATE_ALIVE
        self.board[row + 1][col - 1] = STATE_ALIVE

    def init_spaceship(self, row, col):
        """Initialize a spaceship"""
        self.board[row - 1][col - 1] = STATE_ALIVE
        self.board[row - 1][col + 2] = STATE_ALIVE
        self.board[row][col - 2] = STATE_ALIVE
        self.board[row + 1][col - 2] = STATE_ALIVE
        self.board[row + 1][col + 2] = STATE_ALIVE
        self.board[row + 2][col - 2] = STATE_ALIVE
        self.board[row + 2][col - 1] = STATE_ALIVE
        self.board[row + 2][col] = STATE_ALIVE
        self.board[row + 2][col + 1] = STATE_ALIVE
        self.board[row + 2][col + 2] = STATE_ALIVE

    def apply_rules(self):
        """Apply rules to the board cells"""
        new_board = copy.deepcopy(self.board)
        for row in range(self.rows):
            for col in range(self.columns):
                neighbors = self.alive_neighbors(row, col)
                if self.board[row][col] == STATE_ALIVE and (neighbors < 2 or neighbors > 3):
                    new_board[row][col] = STATE_DEAD
                elif self.board[row][col] == STATE_DEAD and neighbors == 3:
                    new_board[row][col] = STATE_ALIVE
        self.board = new_board

    def alive_neighbors(self, row, col):
        """Count alive neighbors for a given cell"""
        neighbors = 0

        if row > 0 and self.board[row - 1][col] > 0: # North
            neighbors += 1
        if row > 0 and col < self.columns - 1 and self.board[row - 1][col + 1] > 0: # North East
            neighbors += 1
        if col < self.columns - 1 and self.board[row][col + 1] > 0: # East
            neighbors += 1
        if row < self.rows - 1 and col < self.columns - 1 and self.board[row + 1][col + 1] > 0: # South East
            neighbors += 1
        if row < self.rows - 1 and self.board[row + 1][col] > 0: # South
            neighbors += 1
        if row < self.rows - 1 and col > 0 and self.board[row + 1][col - 1] > 0: # South West
            neighbors += 1
        if col > 0 and self.board[row][col - 1] > 0: # West
            neighbors += 1
        if row > 0 and col > 0 and self.board[row - 1][col - 1] > 0: # North West
            neighbors += 1

        return neighbors

    def draw(self, screen):
        """Draw the board on screen"""
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == STATE_ALIVE:
                    pygame.draw.rect(screen, "white", pygame.Rect(
                        self.gap + (col * self.size) + (col * self.gap),
                        self.gap + (row * self.size) + (row * self.gap),
                        self.size, self.size))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description ='John Conway\'s Game of Life')

    parser.add_argument('-f', '--fps',
                        action='store', dest='fps', type=int, default=10,
                        help='number of frames per second', metavar='fps')

    parser.add_argument('-c', '--columns',
                        action='store', dest='columns', type=int, default=80,
                        help='number of columns', metavar='columns')

    parser.add_argument('-r', '--rows',
                        action='store', dest='rows', type=int, default=60,
                        help='number of rows', metavar='rows')

    parser.add_argument('-s', '--size',
                        action='store', dest='size', type=int, default=10,
                        help='size of a cell in pixels', metavar='size')

    parser.add_argument('-g', '--gap',
                        action='store', dest='gap', type=int, default=2,
                        help='gap between cells in pixels', metavar='gap')

    args = parser.parse_args()

    game = GameOfLife(args)
    game.run_loop()
