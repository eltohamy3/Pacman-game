# --- Importing necessary libraries ---
import pygame  # For creating the game window and handling game graphics/input
import sys     # For system-specific parameters and functions (not used in this snippet)
import random  # For generating random numbers (not used in this snippet)
from collections import deque  # For efficient queue operations (used in BFS algorithm)

# --- Initialize pygame ---
pygame.init()
pygame.font.init()

# --- Game constants ---
TILE_SIZE = 24  # Size of each tile in pixels
GRID_WIDTH, GRID_HEIGHT = 28, 21  # Grid size in tiles (columns x rows)
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT  # Window dimensions

# --- Create game window ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CS188 Pacman")

# --- Define colors in RGB format ---
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PACMAN_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
SCORE_YELLOW = (255, 204, 0)
RED = (255, 0, 0)

# --- Maze layout ---
# 1 represents a wall, 0 represents a path (empty tile where Pacman can move)
maze = [
    [1]*28,  # Top border of the maze
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
    [1]*28, [1]*28, [1]*28, [1]*28  # Bottom borders of the maze
]

# --- Initial positions ---
pacman_pos = [13, 5]  # Starting tile position of Pacman
ghost_pos = [1, 1]    # Starting tile position of the ghost
ghost_timer = 0       # Timer for ghost movement speed control
ghost_speed = 10      # Lower value = faster ghost
score = 0             # Initial score

# --- Pellet Map ---
# pellets[y][x] = True if pellet is at position (x, y)
pellets = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
for y in range(len(maze)):
    for x in range(len(maze[0])):
        if maze[y][x] == 0:
            pellets[y][x] = True  # Place pellet in all empty tiles

# --- Font setup ---
font = pygame.font.SysFont('arial', 28, bold=True)

# --- Function to check valid movement ---
def can_move(x, y):
    # Returns True if the (x, y) tile is inside the grid and not a wall
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        return maze[y][x] == 0
    return False

# --- Ghost AI using Breadth-First Search (BFS) ---
def bfs(start, goal):
    queue = deque()
    queue.append((start, [start]))  # Initialize queue with start path
    visited = set()
    visited.add(tuple(start))  # Mark starting point as visited

    while queue:
        (x, y), path = queue.popleft()
        if [x, y] == goal:
            return path  # Return the shortest path to goal
        # Try moving in 4 directions
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if can_move(nx, ny) and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [[nx, ny]]))
                visited.add((nx, ny))
    return [start]  # No path found

# --- Draw background with a gradient on valid paths ---
def draw_gradient():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 0:
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                intensity = int(100 + 155 * (y / GRID_HEIGHT))  # Create gradient effect
                pygame.draw.rect(screen, (intensity, intensity//2, intensity//3), rect)

# --- Draw walls (black blocks with blue borders) ---
def draw_walls():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maze[y][x] == 1:
                rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, BLUE, rect, 2)

# --- Main Game Loop ---
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)  # Limit FPS to 60
    screen.fill(BLACK)  # Clear screen

    # --- Handle Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game loop

    # --- Handle Pacman Input ---
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
        pellets[py][px] = False  # Remove pellet from map
        score += 10  # Increase score

    # --- Move Ghost using BFS pathfinding ---
    ghost_timer += 1
    if ghost_timer >= ghost_speed:
        ghost_timer = 0
        path = bfs(ghost_pos, pacman_pos)  # Calculate shortest path to Pacman
        if len(path) > 1:
            ghost_pos = path[1]  # Move ghost one step closer

    # --- Check Collision ---
    if pacman_pos == ghost_pos:
        print("Game Over")
        running = False

    # --- Draw everything ---
    draw_gradient()  # Background
    draw_walls()     # Maze

    # --- Draw pellets ---
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if pellets[y][x]:
                cx = x * TILE_SIZE + TILE_SIZE // 2
                cy = y * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, WHITE, (cx, cy), 4)

    # --- Draw Pacman ---
    pac_x = pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2
    pac_y = pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, PACMAN_YELLOW, (pac_x, pac_y), TILE_SIZE//2 - 2)
    # Draw Pacman mouth
    pygame.draw.polygon(screen, BLACK, [(pac_x, pac_y), (pac_x + 10, pac_y - 10), (pac_x + 10, pac_y + 10)])

    # --- Draw Ghost ---
    ghost_x = ghost_pos[0] * TILE_SIZE + TILE_SIZE // 2
    ghost_y = ghost_pos[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, RED, (ghost_x, ghost_y), TILE_SIZE//2 - 2)

    # --- Draw Score ---
    score_surf = font.render(f"SCORE:  {score}", True, SCORE_YELLOW)
    screen.blit(score_surf, (10, HEIGHT - 40))  # Draw score text near bottom-left

    pygame.display.flip()  # Update the screen

# --- Exit Pygame ---
pygame.quit()
