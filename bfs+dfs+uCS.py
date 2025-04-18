# --- Pacman Game (DFS, BFS, UCS with Visualized Path & Visited Nodes) ---
import pygame
import time
import heapq
from collections import deque
from mazeLayouts import mazeLayouts

pygame.init()
pygame.font.init()

# Constants
TILE_SIZE = 21
GRID_WIDTH, GRID_HEIGHT = 37, 37
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT
SEARCH_ALGO = 'ucs'  # Change to 'bfs', 'dfs', or 'ucs'

pacman_img = pygame.image.load("assets/pacman_right.png")
pacman_img = pygame.transform.scale(pacman_img, (TILE_SIZE, TILE_SIZE))

# Colors
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
GOAL_COLOR = (255, 0, 0)
GREEN = (0, 255, 0)
PATH_COLOR = (255, 165, 0)  # Orange
VISITED_COLOR = (100, 149, 237)  # Cornflower blue

BIGMAZE = mazeLayouts.BIGMAZE

class Maze:
    def __init__(self):
        self.layout = BIGMAZE

    def can_move(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.layout[y][x] == 0

    def draw(self, screen, goal, visited, path):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, TEAL, rect)

        for x, y in visited:
            pygame.draw.rect(screen, VISITED_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        for x, y in path:
            pygame.draw.rect(screen, PATH_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        if goal:
            gx, gy = goal
            pygame.draw.circle(screen, GOAL_COLOR, (gx * TILE_SIZE + TILE_SIZE // 2, gy * TILE_SIZE + TILE_SIZE // 2), 6)

class Pacman:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.path = []
        self.reached_goal = False

    def move_along_path(self):
        if self.path:
            self.pos = self.path.pop(0)
            pygame.time.wait(100)
            if not self.path:
                self.reached_goal = True

    def draw(self, screen):
        x = self.pos[0] * TILE_SIZE
        y = self.pos[1] * TILE_SIZE
        screen.blit(pacman_img, (x, y))

# --- DFS Implementation ---
def dfs(maze, start, goal):
    stack = [start]
    visited = set()
    parent = {}
    visited.add(start)

    while stack:
        current = stack.pop()
        if current == goal:
            break
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if maze.can_move(nx, ny) and (nx, ny) not in visited:
                stack.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return [], visited
    path.reverse()
    return path, visited

# --- BFS Implementation ---
def bfs(maze, start, goal):
    queue = deque([start])
    visited = set()
    parent = {}
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if maze.can_move(nx, ny) and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return [], visited
    path.reverse()
    return path, visited

# --- UCS Implementation ---
def ucs(maze, start, goal):
    pq = []
    heapq.heappush(pq, (0, start))
    visited = set()
    parent = {}
    cost_so_far = {start: 0}

    while pq:
        cost, current = heapq.heappop(pq)
        visited.add(current)
        if current == goal:
            break

        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)
            new_cost = cost + 1  # cost for each move is 1

            if maze.can_move(nx, ny) and (next_node not in cost_so_far or new_cost < cost_so_far[next_node]):
                cost_so_far[next_node] = new_cost
                heapq.heappush(pq, (new_cost, next_node))
                parent[next_node] = current

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return [], visited
    path.reverse()
    return path, visited

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman - DFS, BFS, UCS")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.maze = Maze()
        self.start_pos = (1, 1)
        self.goal_pos = (35, 35)
        self.pacman = Pacman(*self.start_pos)
        self.running = True
        self.start_time = time.time()
        self.end_time = None

        # Compute path
        if SEARCH_ALGO == 'dfs':
            self.pacman.path, self.visited_nodes = dfs(self.maze, self.start_pos, self.goal_pos)
        elif SEARCH_ALGO == 'bfs':
            self.pacman.path, self.visited_nodes = bfs(self.maze, self.start_pos, self.goal_pos)
        elif SEARCH_ALGO == 'ucs':
            self.pacman.path, self.visited_nodes = ucs(self.maze, self.start_pos, self.goal_pos)
        else:
            print(f"Unknown search algorithm: {SEARCH_ALGO}")
            self.visited_nodes = set()

        self.original_path = list(self.pacman.path)

    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen, self.goal_pos, self.visited_nodes, self.original_path)
        self.pacman.draw(self.screen)

        if self.pacman.reached_goal:
            self.end_time = self.end_time or time.time()
            elapsed = round(self.end_time - self.start_time, 2)
            win_text = self.font.render(f"{SEARCH_ALGO.upper()} - Goal Reached in {elapsed}s!", True, GREEN)
            self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    def update(self):
        if not self.pacman.reached_goal:
            self.pacman.move_along_path()

    def run(self):
        while self.running:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.update()
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
