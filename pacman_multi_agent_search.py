
# --- Pacman Game with Multiple Search Algorithms & Visual Feedback ---
import pygame
import time
from collections import deque
import heapq
from mazeLayouts import mazeLayouts

pygame.init()
pygame.font.init()

# Constants
TILE_SIZE = 21
# GRID_WIDTH, GRID_HEIGHT = 37, 37
GRID_WIDTH, GRID_HEIGHT = 31, 15
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT
SEARCH_ALGO = 'dfs'

pacman_img = pygame.image.load("assets/pacman_right.png")
pacman_img = pygame.transform.scale(pacman_img, (TILE_SIZE, TILE_SIZE))


# Colors
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
GOAL_COLOR = (255, 0, 0)
GREEN = (0, 255, 0)
PATH_COLOR = (255, 165, 0)
VISITED_COLOR = (100, 149, 237)

# 31 * 15
BIGSEARCH = mazeLayouts.BIGSEARCH

# 37* 37
BIGMAZE = mazeLayouts.BIGMAZE
class Maze:
    def __init__(self):
        self.layout = BIGSEARCH

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
            pygame.time.wait(80)
            if not self.path:
                self.reached_goal = True

    def draw(self, screen):
        x = self.pos[0] * TILE_SIZE
        y = self.pos[1] * TILE_SIZE
        screen.blit(pacman_img, (x, y))

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
    return reconstruct_path(start, goal, parent), visited

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
    return reconstruct_path(start, goal, parent), visited

def ucs(maze, start, goal):
    heap = [(0, start)]
    visited = set()
    parent = {}
    cost_so_far = {start: 0}
    while heap:
        cost, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            break
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)
            new_cost = cost + 1
            if maze.can_move(nx, ny) and (next_node not in cost_so_far or new_cost < cost_so_far[next_node]):
                cost_so_far[next_node] = new_cost
                heapq.heappush(heap, (new_cost, next_node))
                parent[next_node] = current
    return reconstruct_path(start, goal, parent), visited

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, goal):
    heap = [(0, start)]
    parent = {}
    g = {start: 0}
    visited = set()
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        visited.add(current)
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)
            new_g = g[current] + 1
            if maze.can_move(nx, ny) and (next_node not in g or new_g < g[next_node]):
                g[next_node] = new_g
                f = new_g + heuristic(next_node, goal)
                heapq.heappush(heap, (f, next_node))
                parent[next_node] = current
    return reconstruct_path(start, goal, parent), visited

def greedy(maze, start, goal):
    heap = [(heuristic(start, goal), start)]
    parent = {}
    visited = set()
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)
            if maze.can_move(nx, ny) and next_node not in visited:
                heapq.heappush(heap, (heuristic(next_node, goal), next_node))
                parent[next_node] = current
    return reconstruct_path(start, goal, parent), visited

def reconstruct_path(start, goal, parent):
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return []
    path.reverse()
    return path

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman Multi-Agent Search")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 20, bold=True)
        self.maze = Maze()
        self.start_pos = (1, 1)
        self.goal_pos = (29, 13)
        self.running = True
        self.start_menu()

    def set_algorithm(self, name):
        self.algorithm = name
        self.pacman = Pacman(*self.start_pos)
        self.start_time = time.time()
        self.end_time = None
        search_fn = {'dfs': dfs, 'bfs': bfs, 'ucs': ucs, 'astar': a_star, 'greedy': greedy}.get(name)
        if search_fn:
            self.pacman.path, self.visited_nodes = search_fn(self.maze, self.start_pos, self.goal_pos)
            self.original_path = list(self.pacman.path)
        else:
            self.visited_nodes = set()
            self.original_path = []

    def draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen, self.goal_pos, self.visited_nodes, self.original_path)
        self.pacman.draw(self.screen)

        if self.pacman.reached_goal:
            self.end_time = self.end_time or time.time()
            elapsed = round(self.end_time - self.start_time, 2)
            stats = [
                f"{self.algorithm.upper()} - Goal Reached!",
                f"Time: {elapsed}s",
                f"Visited: {len(self.visited_nodes)}",
                f"Path Length: {len(self.original_path)}",
                "Press R to Restart or Q to Quit"
            ]
            for i, line in enumerate(stats):
                txt = self.font.render(line, True, GREEN)
                self.screen.blit(txt, (10, HEIGHT - (len(stats)-i)*24))

        pygame.display.flip()

    def update(self):
        if not self.pacman.reached_goal:
            self.pacman.move_along_path()

    def start_menu(self):
        selecting = True
        while selecting:
            self.screen.fill(BLACK)
            title = self.font.render("Select Search Algorithm", True, GREEN)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            options = [
                ("1 - DFS", pygame.K_1),
                ("2 - BFS", pygame.K_2),
                ("3 - UCS", pygame.K_3),
                ("4 - A*", pygame.K_4),
                ("5 - Greedy Best-First", pygame.K_5),
            ]

            for i, (text, _) in enumerate(options):
                option_text = self.font.render(text, True, WHITE)
                self.screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 120 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    keys = {
                        pygame.K_1: 'dfs',
                        pygame.K_2: 'bfs',
                        pygame.K_3: 'ucs',
                        pygame.K_4: 'astar',
                        pygame.K_5: 'greedy',
                    }
                    if event.key in keys:
                        self.set_algorithm(keys[event.key])
                        selecting = False

    def reset(self):

        # Show the menu again
        self.start_menu()

        # Recreate Pacman and rerun the selected search
        self.pacman = Pacman(*self.start_pos)
        self.start_time = time.time()
        self.end_time = None
        search_fn = {'dfs': dfs, 'bfs': bfs, 'ucs': ucs, 'astar': a_star, 'greedy': greedy}.get(self.algorithm)
        if search_fn:
            self.pacman.path, self.visited_nodes = search_fn(self.maze, self.start_pos, self.goal_pos)
            self.original_path = list(self.pacman.path)
        else:
            self.visited_nodes = set()
            self.original_path = []

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.pacman.reached_goal:
                        if event.key == pygame.K_r:
                            self.reset()
                        elif event.key == pygame.K_q:
                            self.running = False

            self.update()
            self.draw()
        pygame.quit()



if __name__ == "__main__":
    game = Game()
    game.run()
