# --- Pacman Game (Single Agent) ---
import pygame
import sys
from mazeLayouts import mazeLayouts

# --- Initialize pygame ---
pygame.init()
pygame.font.init()

# --- Constants ---
TILE_SIZE = 21
GRID_WIDTH, GRID_HEIGHT = 31, 15

# GRID_WIDTH, GRID_HEIGHT = 37 , 37

WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT

# Load Pacman images
pacman_right_img = pygame.image.load("assets/pacman-right/1.png")
pacman_right_img = pygame.transform.scale(pacman_right_img, (TILE_SIZE, TILE_SIZE))

pacman_left_img = pygame.image.load("assets/pacman-left/1.png")
pacman_left_img = pygame.transform.scale(pacman_left_img, (TILE_SIZE, TILE_SIZE))

pacman_up_img = pygame.image.load("assets/pacman-up/1.png")
pacman_up_img = pygame.transform.scale(pacman_up_img, (TILE_SIZE, TILE_SIZE))

pacman_down_img = pygame.image.load("assets/pacman-down/1.png")
pacman_down_img = pygame.transform.scale(pacman_down_img, (TILE_SIZE, TILE_SIZE))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCORE_YELLOW = (255, 204, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
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
        if maze.can_move(new_x, new_y):
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
        screen.blit(pacman_right_img, (x - 8, y - 8))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Single Agent Pacman")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 28, bold=True)
        self.small_font = pygame.font.SysFont('arial', 20, bold=True)
        self.maze = Maze()
        self.pacman = Pacman(13, 5)
        self.running = True
        self.pacman_win = False

    def all_pellets_eaten(self):
        for row in self.maze.pellets:
            if any(row):
                return False
        return True

    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw_gradient(self.screen)
        self.maze.draw_pellets(self.screen)
        self.pacman.draw(self.screen)

        # Draw score
        score_text = self.small_font.render(f'Score: {self.pacman.score}', True, SCORE_YELLOW)
        self.screen.blit(score_text, (10, HEIGHT - 30))

        if self.pacman_win:
            win_text = self.font.render('YOU WIN', True, GREEN)
            score_text = self.font.render(f'Final Score: {self.pacman.score}', True, SCORE_YELLOW)
            restart_text = self.small_font.render('Press R to Restart', True, WHITE)
            self.screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 50))
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

        pygame.display.flip()

    def update(self):
        if not self.pacman_win:
            self.pacman.update(self.maze)
            if self.all_pellets_eaten():
                self.pacman_win = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.pacman_win:
                        self.maze = Maze()
                        self.pacman = Pacman(13, 5)
                        self.pacman_win = False
            self.update()
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
