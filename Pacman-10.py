import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 400
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pacman")

# Clock
clock = pygame.time.Clock()

# Create a simple map: 0 = empty, 1 = wall

maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]

# Pacman start position (in grid coordinates)
pacman_pos = [1, 1]

def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            tile = maze[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)

def draw_pacman():
    x = pacman_pos[1] * TILE_SIZE + TILE_SIZE // 2
    y = pacman_pos[0] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, YELLOW, (x, y), TILE_SIZE // 2 - 4)

# Game loop
while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        new_pos = [pacman_pos[0] - 1, pacman_pos[1]]
    elif keys[pygame.K_DOWN]:
        new_pos = [pacman_pos[0] + 1, pacman_pos[1]]
    elif keys[pygame.K_LEFT]:
        new_pos = [pacman_pos[0], pacman_pos[1] - 1]
    elif keys[pygame.K_RIGHT]:
        new_pos = [pacman_pos[0], pacman_pos[1] + 1]
    else:
        new_pos = pacman_pos

    # Check for walls
    if maze[new_pos[0]][new_pos[1]] != 1:
        pacman_pos = new_pos

    draw_maze()
    draw_pacman()

    pygame.display.flip()
