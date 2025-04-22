import math
import pygame
import time
from collections import deque
import heapq
import mazeLayouts

pygame.init()
pygame.font.init()

# Constants
TILE_SIZE = 21
GRID_WIDTH, GRID_HEIGHT = 31, 15
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH + 10, TILE_SIZE * GRID_HEIGHT + 10

# Load and scale images
# pacman_right_img = pygame.image.load("assets/pacman_right.png")
# pacman_right_img = pygame.transform.scale(pacman_right_img, (TILE_SIZE, TILE_SIZE))
#
# pacman_left_img = pygame.image.load("assets/pacman_left.png")
# pacman_left_img = pygame.transform.scale(pacman_left_img, (TILE_SIZE, TILE_SIZE))
#
# pacman_up_img = pygame.image.load("assets/pacman_up.png")
# pacman_up_img = pygame.transform.scale(pacman_up_img, (TILE_SIZE, TILE_SIZE))
#
# pacman_down_img = pygame.image.load("assets/pacman_down.png")
# pacman_down_img = pygame.transform.scale(pacman_down_img, (TILE_SIZE, TILE_SIZE))

pacman_right_path = [ "assets/pacman-right/1.png" ,
                      "assets/pacman-right/2.png" ,
                      "assets/pacman-right/3.png" ]

pacman_left_path = [ "assets/pacman-left/1.png" ,
                     "assets/pacman-left/2.png" ,
                     "assets/pacman-left/3.png" ]

pacman_up_path = [ "assets/pacman-up/1.png" ,
                   "assets/pacman-up/2.png" ,
                   "assets/pacman-up/3.png" ]

pacman_down_path = [ "assets/pacman-down/1.png" ,
                     "assets/pacman-down/2.png" ,
                     "assets/pacman-down/3.png" ]


# Colors
BLUE = (24, 24, 217)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
GOAL_COLOR = (255, 0, 0)
GREEN = (0, 255, 0)
PATH_COLOR = (168, 92, 83)
VISITED_COLOR = (82, 80, 80)
DOT_COLOR = (255, 255, 0)  # Yellow dots

# Load maze layouts
BIGSEARCH = mazeLayouts.BIGSEARCH
BIGMAZE = mazeLayouts.BIGMAZE


class Maze:
    def __init__(self):
        self.layout = BIGSEARCH
        # Find all goal positions (all empty spaces)
        self.goals = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0:
                    self.goals.append((x, y))

        # 2D array to track uneaten dots (True = uneaten, False = eaten)
        self.uneaten = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for x, y in self.goals:
            self.uneaten[y][x] = True

    def can_move(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.layout[y][x] == 0

    def eat_dot(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.uneaten[y][x] = False

    def is_dot_uneaten(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.uneaten[y][x]
        return False

    def get_uneaten_dots(self):
        uneaten_dots = set()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.is_dot_uneaten(x, y):
                    uneaten_dots.add((x, y))
        return uneaten_dots

    def all_dots_eaten(self):
        return len(self.get_uneaten_dots()) == 0

    def draw(self, screen, visited, path, current_path=None):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0 or self.layout[y][x] == 2:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 1.6, TILE_SIZE * 1.6)
                    pygame.draw.rect(screen, BLACK, rect)

        # Color all the nodes that have been visited
        for x, y in visited:
            pygame.draw.rect(screen, VISITED_COLOR, (x * TILE_SIZE + 7, y * TILE_SIZE + 7, TILE_SIZE, TILE_SIZE))

        # Color the current path
        if current_path:
            for x, y in current_path:
                pygame.draw.rect(screen, PATH_COLOR, (x * TILE_SIZE + 7, y * TILE_SIZE + 7, TILE_SIZE, TILE_SIZE))

        # Draw dots for goals that haven't been eaten yet
        for x, y in self.get_uneaten_dots():
            pygame.draw.circle(screen, DOT_COLOR, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 4)


class Pacman:
    def __init__(self, x, y, maze):
        self.pos = (x, y)  # Store as tuple for consistency
        self.prevPos = (x, y)  # Store as tuple for consistency
        self.path = []
        self.maze = maze
        self.all_goals_reached = False
        self.visited_nodes = set()
        self.current_path = []
        self.next_goal = None
        self.frame_idx = 0
        self.dir = "r"

        # Eat the starting position dot
        self.maze.eat_dot(x, y)

    def find_next_path(self, algorithm):
        # Reset current path
        self.current_path = []

        # Get the remaining uneaten dots
        uneaten_dots = self.maze.get_uneaten_dots()

        if not uneaten_dots:
            self.all_goals_reached = True
            return

        # Find the next goal based on the algorithm
        if algorithm == 'dfs':
            self.next_goal, self.current_path, visited = find_next_goal_dfs(self.maze, self.pos, uneaten_dots)
        elif algorithm == 'bfs':
            self.next_goal, self.current_path, visited = find_next_goal_bfs(self.maze, self.pos, uneaten_dots)
        elif algorithm == 'ucs':
            self.next_goal, self.current_path, visited = find_next_goal_ucs(self.maze, self.pos, uneaten_dots)
        elif algorithm == 'astar':
            self.next_goal, self.current_path, visited = find_next_goal_astar(self.maze, self.pos, uneaten_dots)
        elif algorithm == 'greedy':
            self.next_goal, self.current_path, visited = find_next_goal_greedy(self.maze, self.pos, uneaten_dots)
        else:
            self.next_goal, self.current_path, visited = find_next_goal_bfs(self.maze, self.pos, uneaten_dots)

        # Update visited nodes
        self.visited_nodes.update(visited)

    def move(self):
        if self.current_path:
            self.prevPos = self.pos
            self.pos = self.current_path.pop(0)

            # Eat the dot
            self.maze.eat_dot(self.pos[0], self.pos[1])

            # Check if we've reached all goals
            if self.maze.all_dots_eaten():
                self.all_goals_reached = True

            return True
        return False

    # def draw(self, screen):
    #     x = self.pos[0] * TILE_SIZE
    #     y = self.pos[1] * TILE_SIZE
    #     if (self.prevPos[0] - self.pos[0] == 1 and self.prevPos[1] - self.pos[1] == 0):
    #         screen.blit(pacman_left_img, (x, y))
    #     elif (self.prevPos[0] - self.pos[0] == -1 and self.prevPos[1] - self.pos[1] == 0):
    #         screen.blit(pacman_right_img, (x, y))
    #     elif (self.prevPos[0] - self.pos[0] == 0 and self.prevPos[1] - self.pos[1] == -1):
    #         screen.blit(pacman_down_img, (x, y))
    #     elif (self.prevPos[0] - self.pos[0] == 0 and self.prevPos[1] - self.pos[1] == 1):
    #         screen.blit(pacman_up_img, (x, y))
    #     else:
    #         screen.blit(pacman_right_img, (x, y))  # Default
    def get_direction ( self , screen ) :
        (pos_x , pos_y) = (self.prevPos [0] - self.pos [0] , self.prevPos [1] - self.pos [1])
        self.dir = { (-1 , 0) : 'r' , (1 , 0) : 'l' , (0 , -1) : 'd' , (0 , 1) : 'u' }.get ( (pos_x , pos_y) )

    def update_frame ( self , screen ) :
        x = self.pos [0] * TILE_SIZE
        y = self.pos [1] * TILE_SIZE
        pacman_dir = { 'r' : pacman_right_path , 'l' : pacman_left_path , 'u' : pacman_up_path ,
                       'd' : pacman_down_path }.get ( self.dir )
        self.frame_idx = self.frame_idx % len ( pacman_dir )
        pacman_img = pygame.image.load ( pacman_dir [self.frame_idx] )
        pacman_img = pygame.transform.scale ( pacman_img , (TILE_SIZE , TILE_SIZE) )
        screen.blit ( pacman_img , (x , y) )
        self.frame_idx += 1

    def draw ( self , screen ) :
        self.get_direction ( screen )
        self.update_frame ( screen )


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


def find_next_goal_dfs(maze, start, goals_to_visit):
    stack = [start]
    visited = set([start])
    parent = {}

    while stack:
        node = stack.pop()

        # Check if this is a goal
        if node in goals_to_visit:
            return node, reconstruct_path(start, node, parent), visited

        x, y = node
        # Try all four directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)
            if maze.can_move(nx, ny) and next_node not in visited:
                stack.append(next_node)
                visited.add(next_node)
                parent[next_node] = node

    # No path found to any goal
    return None, [], visited


def find_next_goal_bfs(maze, start, goals_to_visit):
    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        node = queue.popleft()

        # Check if this is a goal
        if node in goals_to_visit:
            return node, reconstruct_path(start, node, parent), visited

        x, y = node
        # Try all four directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)
            if maze.can_move(nx, ny) and next_node not in visited:
                queue.append(next_node)
                visited.add(next_node)
                parent[next_node] = node

    # No path found to any goal
    return None, [], visited


def find_next_goal_ucs(maze, start, goals_to_visit):
    heap = [(0, start)]
    visited = set()
    parent = {}
    cost_so_far = {start: 0}

    while heap:
        cost, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        # Check if this is a goal
        if node in goals_to_visit:
            return node, reconstruct_path(start, node, parent), visited

        x, y = node
        # Try all four directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)
            new_cost = cost_so_far[node] + 1

            if maze.can_move(nx, ny) and (next_node not in cost_so_far or new_cost < cost_so_far[next_node]):
                cost_so_far[next_node] = new_cost
                heapq.heappush(heap, (new_cost, next_node))
                parent[next_node] = node

    # No path found to any goal
    return None, [], visited


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance


def find_next_goal_astar(maze, start, goals_to_visit):
    # Find the minimum estimated cost to any goal
    open_set = []
    for goal in goals_to_visit:
        heapq.heappush(open_set, (heuristic(start, goal), goal))

    # A* to the nearest goal by estimated distance
    closest_goals = []
    for _ in range(min(3, len(goals_to_visit))):  # Check the top 3 closest goals
        if open_set:
            _, goal = heapq.heappop(open_set)
            closest_goals.append(goal)

    # Now run A* to find the actual closest goal
    best_path = []
    best_goal = None
    all_visited = set()

    for goal in closest_goals:
        heap = [(0, start)]
        visited = set()
        parent = {}
        g = {start: 0}
        f = {start: heuristic(start, goal)}

        while heap:
            _, current = heapq.heappop(heap)

            if current == goal:
                path = reconstruct_path(start, goal, parent)
                if not best_path or len(path) < len(best_path):
                    best_path = path
                    best_goal = goal
                break

            visited.add(current)

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                next_node = (nx, ny)

                if maze.can_move(nx, ny):
                    new_g = g[current] + 1

                    if next_node not in g or new_g < g[next_node]:
                        g[next_node] = new_g
                        f_val = new_g + heuristic(next_node, goal)
                        f[next_node] = f_val
                        heapq.heappush(heap, (f_val, next_node))
                        parent[next_node] = current

        all_visited.update(visited)

    return best_goal, best_path, all_visited


def find_next_goal_greedy(maze, start, goals_to_visit):
    # Find the closest goal by heuristic
    closest_goal = min(goals_to_visit, key=lambda goal: heuristic(start, goal))

    heap = [(heuristic(start, closest_goal), start)]
    visited = set()
    parent = {}

    while heap:
        _, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        # Check if this is the goal
        if node == closest_goal:
            return node, reconstruct_path(start, node, parent), visited

        x, y = node
        # Try all four directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            next_node = (nx, ny)

            if maze.can_move(nx, ny) and next_node not in visited:
                priority = heuristic(next_node, closest_goal)
                heapq.heappush(heap, (priority, next_node))
                parent[next_node] = node

    # No path found to any goal
    return None, [], visited


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman Game - Eat All Dots (Runtime Algorithm)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 20, bold=True)
        self.maze = Maze()
        self.start_pos = (1, 1)
        self.running = True
        self.algorithm = None
        self.path_history = []  # Track all moves for statistics
        self.start_menu()

    def set_algorithm(self, name):
        self.algorithm = name
        self.maze = Maze()  # Reset maze with all dots
        self.pacman = Pacman(*self.start_pos, self.maze)
        self.path_history = []
        self.start_time = time.time()
        self.end_time = None

        # Find initial path
        self.pacman.find_next_path(name)

    def draw(self):
        self.screen.fill(BLUE)

        # Draw maze, visited nodes, and current path
        self.maze.draw(self.screen, self.pacman.visited_nodes, [], self.pacman.current_path)
        self.pacman.draw(self.screen)

        # Display progress
        goals_eaten = len(self.maze.goals) - len(self.maze.get_uneaten_dots())
        total_goals = len(self.maze.goals)
        progress_text = f"Goals: {goals_eaten}/{total_goals}"
        txt = self.font.render(progress_text, True, WHITE)
        self.screen.blit(txt, (10, 10))

        # Display current algorithm
        algo_text = f"Algorithm: {self.algorithm.upper()}"
        txt = self.font.render(algo_text, True, WHITE)
        self.screen.blit(txt, (WIDTH - txt.get_width() - 10, 10))

        if self.pacman.all_goals_reached:
            self.end_time = self.end_time or time.time()
            elapsed = round(self.end_time - self.start_time, 2)
            stats = [
                f"{self.algorithm.upper()} - All Goals Reached!",
                f"Time: {elapsed}s",
                f"Visited: {len(self.pacman.visited_nodes)}",
                f"Path Length: {len(self.path_history)}",
                "Press R to Restart or Q to Quit"
            ]
            for i, line in enumerate(stats):
                txt = self.font.render(line, True, GREEN)
                self.screen.blit(txt, (10, HEIGHT - (len(stats) - i) * 24))

        pygame.display.flip()

    def update(self):
        if not self.pacman.all_goals_reached:
            # If we have no current path, find the next path
            if not self.pacman.current_path:
                self.pacman.find_next_path(self.algorithm)

            # Move along the current path
            if self.pacman.move():
                self.path_history.append(self.pacman.pos)
                pygame.time.wait(80)  # Delay for visualization

    def start_menu(self):
        selecting = True
        while selecting:
            self.screen.fill(BLACK)
            title = self.font.render("Select Search Algorithm", True, GREEN)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

            options = [
                ("1 - DFS (Runtime)", pygame.K_1),
                ("2 - BFS (Runtime)", pygame.K_2),
                ("3 - UCS (Runtime)", pygame.K_3),
                ("4 - A* (Runtime)", pygame.K_4),
                ("5 - Greedy Best-First (Runtime)", pygame.K_5),
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
        # Show the menu again to select an algorithm
        self.start_menu()

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.pacman.all_goals_reached:
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