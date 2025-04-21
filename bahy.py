# --- Pacman Game ---
import pygame
import sys
import random
from collections import deque

import mazeLayouts.mazeLayouts
from mazeLayouts import mazeLayouts

# --- Initialize pygame ---
pygame.init()
pygame.font.init()

# --- Constants ---
TILE_SIZE = 24
GRID_WIDTH, GRID_HEIGHT = 31, 15
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT

pacman_right_img = pygame.image.load("assets/pacman_right.png")
pacman_right_img = pygame.transform.scale(pacman_right_img, (TILE_SIZE, TILE_SIZE))

pacman_left_img = pygame.image.load("assets/pacman_left.png")
pacman_left_img = pygame.transform.scale(pacman_left_img, (TILE_SIZE, TILE_SIZE))

pacman_up_img = pygame.image.load("assets/pacman_up.png")
pacman_up_img = pygame.transform.scale(pacman_up_img, (TILE_SIZE, TILE_SIZE))

pacman_down_img = pygame.image.load("assets/pacman_down.png")
pacman_down_img = pygame.transform.scale(pacman_down_img, (TILE_SIZE, TILE_SIZE))

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PACMAN_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
SCORE_YELLOW = (255, 204, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)

# 31 * 15
BIGSEARCH = mazeLayouts.BIGSEARCH

# 37* 37
BIGMAZE = mazeLayouts.BIGMAZE

class Maze:
    def __init__(self):
        self.layout = BIGSEARCH
        self.pellets = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(len(self.layout)):
            for x in range(len(self.layout[0])):
                if self.layout[y][x] == 0:
                    self.pellets[y][x] = True

    def can_move(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.layout[y][x] == 0

    def draw_gradient(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0 or self.layout[y][x] == 2:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 1.4, TILE_SIZE * 1.4)
                    pygame.draw.rect(screen, TEAL, rect)

    def draw_pellets(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.pellets[y][x]:
                    cx = x * TILE_SIZE + TILE_SIZE // 2
                    cy = y * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, WHITE, (cx, cy), 4)


class Character:
    def __init__(self, x, y):
        self.pos = [x, y]

    def move(self, dx, dy, maze):
        new_x, new_y = self.pos[0] + dx, self.pos[1] + dy
        if maze.valid(new_x, new_y):
            self.pos = [new_x, new_y]
            pygame.time.wait(100)
            return True
        return False


class Pacman(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score = 0

    def update(self, maze):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.move(-1, 0, maze)
        if keys[pygame.K_RIGHT]: self.move(1, 0, maze)
        if keys[pygame.K_UP]: self.move(0, -1, maze)
        if keys[pygame.K_DOWN]: self.move(0, 1, maze)

        x, y = self.pos
        if maze.pellets[y][x]:
            maze.pellets[y][x] = False
            self.score += 10

    def draw(self, screen):
        x = self.pos[0] * TILE_SIZE + TILE_SIZE // 2
        y = self.pos[1] * TILE_SIZE + TILE_SIZE // 2
        # pygame.draw.circle(screen, PACMAN_YELLOW, (x, y), TILE_SIZE // 2 - 2)
        screen.blit(pacman_right_img, (x - 8, y - 8))


class Ghost(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.timer = 0
        self.speed = 10
        self.mode = "chase"  # chase or random
        self.mode_timer = 0
        self.mode_duration = 300  # frames before switching modes

    def bfs(self, start, goal, maze):
        queue = deque()
        queue.append((start, [start]))
        visited = set([tuple(start)])
        while queue:
            (x, y), path = queue.popleft()
            if [x, y] == goal:
                return path
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if maze.valid(nx, ny) and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [[nx, ny]]))
                    visited.add((nx, ny))
        return [start]

    def get_random_move(self, maze):
        possible_moves = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_x, new_y = self.pos[0] + dx, self.pos[1] + dy
            if maze.valid(new_x, new_y):
                possible_moves.append([new_x, new_y])
        return random.choice(possible_moves) if possible_moves else self.pos

    def update(self, target_pos, maze):
        self.timer += 1
        self.mode_timer += 1

        # Switch between chase and random modes
        if self.mode_timer >= self.mode_duration:
            self.mode_timer = 0
            self.mode = "random" if self.mode == "chase" else "chase"

        if self.timer >= self.speed:
            self.timer = 0
            if self.mode == "chase":
                path = self.bfs(self.pos, target_pos, maze)
                if len(path) > 1:
                    self.pos = path[1]
            else:  # random mode
                self.pos = self.get_random_move(maze)

    def draw(self, screen):
        x = self.pos[0] * TILE_SIZE + TILE_SIZE // 2
        y = self.pos[1] * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, RED, (x, y), TILE_SIZE // 2 - 2)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("OOP Pacman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 28, bold=True)
        self.small_font = pygame.font.SysFont('arial', 20, bold=True)
        self.maze = Maze()
        self.pacman = Pacman(13, 13)
        self.ghost = Ghost(1, 1)
        self.running = True
        self.game_over = False
        self.pacman_win = False


    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw_gradient(self.screen)
        # self.maze.draw_walls(self.screen)
        self.maze.draw_pellets(self.screen)
        self.pacman.draw(self.screen)
        # self.ghost.draw(self.screen)

        # Draw score
        score_text = self.small_font.render(f'Score: {self.pacman.score}', True, SCORE_YELLOW)
        self.screen.blit(score_text, (10, HEIGHT - 30))

        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, RED)
            score_text = self.font.render(f'Final Score: {self.pacman.score}', True, SCORE_YELLOW)
            restart_text = self.small_font.render('Press R to Restart', True, WHITE)

            self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

        # Draw win screen
        if self.pacman_win:
            win_text = self.font.render('YOU WIN', True, GREEN)
            restart_text = self.small_font.render('Press R to Restart', True, WHITE)
            score_text = self.font.render(f'Final Score: {self.pacman.score}', True, SCORE_YELLOW)

            self.screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 50))
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

        pygame.display.flip()


    def all_pellets_eaten(self):
        for row in self.maze.pellets:
            if any(row):
                return False
        return True

    def update(self):
        if not self.game_over and not self.pacman_win:
            self.pacman.update(self.maze)
            self.ghost.update(self.pacman.pos, self.maze)
            if self.pacman.pos == self.ghost.pos:
                self.game_over = True
            if self.all_pellets_eaten():
                self.pacman_win = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and (self.game_over or self.pacman_win):
                        # Reset game
                        self.maze = Maze()
                        self.pacman = Pacman(13, 5)
                        self.ghost = Ghost(1, 1)
                        self.game_over = False
                        self.pacman_win = False
            self.update()
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
