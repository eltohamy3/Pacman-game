import pygame
import sys
import random
from collections import deque

# --- Init ---
pygame.init()
pygame.font.init()
TILE_SIZE = 24
GRID_WIDTH, GRID_HEIGHT = 28, 21
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CS188 Pacman")

# --- Colors ---
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PACMAN_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
SCORE_YELLOW = (255, 204, 0)
RED = (255, 0, 0)

# --- Maze Layout (1 = Wall, 0 = Path) ---
# maze = [
#     [1]*28,
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1],
#     [1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1],
#     [1,0,1,0,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1],
#     [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
#            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
#            [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
#            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
#            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
#            [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
#            [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
#            [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
#
#            [1]*28
# ] + [[1]*28 for _ in range(GRID_HEIGHT - 7)]

maze = [
    [1]*28,
    [1,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,0,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1]*28,
    [1]*28,
    [1]*28,
    [1]*28
]

# --- Init Positions ---
pacman_pos = [13, 5]
ghost_pos = [1, 1]
ghost_timer = 0
ghost_speed = 10
score = 0

# --- Pellet Map ---
pellets = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
for y in range(len(maze)):
    for x in range(len(maze[0])):
        if maze[y][x] == 0:
            pellets[y][x] = True

# --- Font ---
font = pygame.font.SysFont('arial', 28, bold=True)

# --- Movement Check ---
def can_move(x, y):
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        return maze[y][x] == 0
    return False

# --- Ghost BFS AI ---
def bfs(start, goal):
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(tuple(start))

    while queue:
        (x, y), path = queue.popleft()
        if [x, y] == goal:
            return path
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if can_move(nx, ny) and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [[nx, ny]]))
                visited.add((nx, ny))
    return [start]

# --- Gradient Background ---
def draw_gradient():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 0:
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                intensity = int(100 + 155 * (y / GRID_HEIGHT))
                pygame.draw.rect(screen, (intensity, intensity//2, intensity//3), rect)

# --- Wall Outline ---
def draw_walls():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, BLUE, rect, 2)

# --- Game Loop ---
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Input ---
    keys = pygame.key.get_pressed()
    px, py = pacman_pos
    if keys[pygame.K_LEFT] and can_move(px - 1, py):
        pacman_pos[0] -= 1
        pygame.time.wait(100)
    if keys[pygame.K_RIGHT] and can_move(px + 1, py):
        pacman_pos[0] += 1
        pygame.time.wait(100)
    if keys[pygame.K_UP] and can_move(px, py - 1):
        pacman_pos[1] -= 1
        pygame.time.wait(100)
    if keys[pygame.K_DOWN] and can_move(px, py + 1):
        pacman_pos[1] += 1
        pygame.time.wait(100)

    # --- Eat Pellet ---
    px, py = pacman_pos
    if pellets[py][px]:
        pellets[py][px] = False
        score += 10

    # --- Ghost Movement ---
    ghost_timer += 1
    if ghost_timer >= ghost_speed:
        ghost_timer = 0
        path = bfs(ghost_pos, pacman_pos)
        if len(path) > 1:
            ghost_pos = path[1]

    # --- Collision ---
    if pacman_pos == ghost_pos:
        print("Game Over")
        running = False

    # --- Draw ---
    draw_gradient()
    draw_walls()

    # Pellets
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if pellets[y][x]:
                cx = x * TILE_SIZE + TILE_SIZE // 2
                cy = y * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, WHITE, (cx, cy), 4)

    # Pacman (mouth wedge)
    pac_x = pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2
    pac_y = pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, PACMAN_YELLOW, (pac_x, pac_y), TILE_SIZE//2 - 2)
    mouth_rect = pygame.Rect(pac_x, pac_y - 5, TILE_SIZE, 10)
    pygame.draw.polygon(screen, BLACK, [(pac_x, pac_y), (pac_x + 10, pac_y - 10), (pac_x + 10, pac_y + 10)])

    # Ghost
    ghost_x = ghost_pos[0] * TILE_SIZE + TILE_SIZE // 2
    ghost_y = ghost_pos[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, RED, (ghost_x, ghost_y), TILE_SIZE//2 - 2)

    # Score
    score_surf = font.render(f"SCORE:  {score}", True, SCORE_YELLOW)
    screen.blit(score_surf, (10, HEIGHT - 40))

    pygame.display.flip()

pygame.quit()
