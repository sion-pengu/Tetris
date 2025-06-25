# -*- coding: utf-8 -*-
import pygame
import random

# --- 定数定義 ---
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
COLUMNS = 10
ROWS = 20

# 色の定義
COLORS = {
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128),
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'J': (0, 0, 255),
    'L': (255, 165, 0)
}

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

# --- クラス定義 ---
class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[shape]
        self.rotation = 0
        self.blocks = SHAPES[shape]
        self.x = COLUMNS // 2 - len(self.blocks[0]) // 2
        self.y = 0

    def rotate(self):
        self.blocks = [list(row) for row in zip(*self.blocks[::-1])]

    def get_coords(self):
        coords = []
        for i, row in enumerate(self.blocks):
            for j, cell in enumerate(row):
                if cell:
                    coords.append((self.x + j, self.y + i))
        return coords

class TetrisGame:
    def __init__(self):
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current = self.new_tetromino()
        self.drop_timer = 0
        self.drop_speed = 500
        self.last_time = pygame.time.get_ticks()

    def new_tetromino(self):
        return Tetromino(random.choice(list(SHAPES.keys())))

    def valid_position(self, shape, dx=0, dy=0):
        for x, y in shape.get_coords():
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx >= COLUMNS or ny >= ROWS:
                return False
            if ny >= 0 and self.board[ny][nx]:
                return False
        return True

    def lock_tetromino(self):
        for x, y in self.current.get_coords():
            if y < 0:
                self.game_over()
                return
            self.board[y][x] = self.current.color
        self.clear_lines()
        self.current = self.new_tetromino()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared_lines = ROWS - len(new_board)
        for _ in range(cleared_lines):
            new_board.insert(0, [None] * COLUMNS)
        self.board = new_board

    def game_over(self):
        print("Game Over")
        pygame.quit()
        exit()

    def hard_drop(self):
        while self.valid_position(self.current, dy=1):
            self.current.y += 1
        self.lock_tetromino()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > self.drop_speed:
            if self.valid_position(self.current, dy=1):
                self.current.y += 1
            else:
                self.lock_tetromino()
            self.last_time = now

    def move(self, dx):
        if self.valid_position(self.current, dx=dx):
            self.current.x += dx

    def rotate(self):
        original = [row[:] for row in self.current.blocks]
        self.current.rotate()
        if not self.valid_position(self.current):
            self.current.blocks = original

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for y in range(ROWS):
            for x in range(COLUMNS):
                if self.board[y][x]:
                    pygame.draw.rect(screen, self.board[y][x],
                                     (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for x, y in self.current.get_coords():
            pygame.draw.rect(screen, self.current.color,
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()

# --- メイン処理 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = TetrisGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_DOWN:
                    if game.valid_position(game.current, dy=1):
                        game.current.y += 1
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()

        game.update()
        game.draw(screen)
        clock.tick(60)

if __name__ == '__main__':
    main()
