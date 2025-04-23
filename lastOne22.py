import heapq
import math
import random
import pygame
import time
from collections import deque

# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
TILE_SIZE = 21
GRID_WIDTH, GRID_HEIGHT = 31, 15
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH + 10, TILE_SIZE * GRID_HEIGHT + 10

# Colors
BLUE = (24, 24, 217)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOAL_COLOR = (255, 0, 0)
GREEN = (0, 255, 0)
DOT_COLOR = (255, 255, 0)  # Yellow dots
GHOST_COLOR = (255, 0, 0)  # Red ghost
WALL_COLOR = (0, 0, 139)  # Darker blue for walls

# Maze layout (same as before)
BIGSEARCH = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Maze:
    def __init__(self):
        self.layout = BIGSEARCH
        self.goals = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0:
                    self.goals.append((x, y))

        self.uneaten = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for x, y in self.goals:
            self.uneaten[y][x] = True

    def can_move(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.layout[y][x] in [0, 2]

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

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 1:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                elif self.layout[y][x] in [0, 2]:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 1.6, TILE_SIZE * 1.6)
                    pygame.draw.rect(screen, BLACK, rect)

        for x, y in self.get_uneaten_dots():
            pygame.draw.circle(screen, DOT_COLOR, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 4)

class Ghost:
    def __init__(self, x, y, maze, game):
        self.pos = (x, y)
        self.prevPos = (x, y)
        self.maze = maze
        self.game = game
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.path = []
        self.speed = 0.3  # Slower than Pacman
        self.move_counter = 0

    def find_path_to_pacman(self, pacman_pos):
        # Use A* instead of BFS for better pathfinding
        open_set = [(0, self.pos)]  # (priority, position)
        came_from = {}
        g_score = {self.pos: 0}
        f_score = {self.pos: manhattan_distance(self.pos, pacman_pos)}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == pacman_pos:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                self.path = path[::-1][:3]  # Only look 3 steps ahead
                return
                
            for dx, dy in self.moves:
                neighbor = (current[0] + dx, current[1] + dy)
                if not self.maze.can_move(*neighbor):
                    continue
                    
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + manhattan_distance(neighbor, pacman_pos)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        self.path = []  # No path found
    def move(self, pacman_pos):
        self.move_counter += 1
        if self.move_counter < 1/self.speed:
            return False
            
        self.move_counter = 0
        self.prevPos = self.pos
        self.find_path_to_pacman(pacman_pos)
        if self.path:
            self.pos = self.path[0]
            return True
        return False

    def draw(self, screen):
        x, y = self.pos
        ghost_rect = pygame.Rect(x * TILE_SIZE + 2, y * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4)
        pygame.draw.rect(screen, GHOST_COLOR, ghost_rect)
        eye_radius = 3
        left_eye_pos = (x * TILE_SIZE + 7, y * TILE_SIZE + 7)
        right_eye_pos = (x * TILE_SIZE + TILE_SIZE - 7, y * TILE_SIZE + 7)
        pygame.draw.circle(screen, WHITE, left_eye_pos, eye_radius)
        pygame.draw.circle(screen, WHITE, right_eye_pos, eye_radius)

    def get_rect(self):
        return pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)

import math
from collections import deque
import heapq
import time

import math
from collections import deque
import heapq

class MinimaxAgent:
    def __init__(self, depth=3):
        self.depth = depth
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.path_cache = {}
        self.ghost_danger_cache = {}
        self.last_dot_path = []
        
    def bfs_shortest_path(self, start, target, maze):
        """Calculate actual shortest path distance considering walls"""
        if start == target:
            return 0, [start]
            
        cache_key = (start, target)
        if cache_key in self.path_cache:
            return self.path_cache[cache_key]
            
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            pos, path = queue.popleft()
            
            for dx, dy in self.moves:
                new_pos = (pos[0] + dx, pos[1] + dy)
                if new_pos == target:
                    result = (len(path), path)
                    self.path_cache[cache_key] = result
                    return result
                    
                if maze.can_move(*new_pos) and new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
        
        # No path found (shouldn't happen in valid maze)
        return float('inf'), []

    def calculate_ghost_danger(self, ghost_pos, maze, steps=3):
        """Calculate all positions ghost could reach in next N steps"""
        cache_key = (*ghost_pos, steps)
        if cache_key in self.ghost_danger_cache:
            return self.ghost_danger_cache[cache_key]
            
        danger_zones = set()
        queue = deque([(ghost_pos, 0)])
        visited = set([ghost_pos])
        
        while queue:
            pos, current_steps = queue.popleft()
            danger_zones.add(pos)
            
            if current_steps >= steps:
                continue
                
            for dx, dy in self.moves:
                new_pos = (pos[0] + dx, pos[1] + dy)
                if maze.can_move(*new_pos) and new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, current_steps + 1))
        
        self.ghost_danger_cache[cache_key] = danger_zones
        return danger_zones

    def evaluationFunction(self, pacman_pos, ghost_pos, maze):
        """Advanced evaluation considering paths and walls"""
        score = 0
        immediate_danger = False
        
        # 1. GHOST DANGER ASSESSMENT (survival first)
        ghost_dist, ghost_path = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        danger_zones = self.calculate_ghost_danger(ghost_pos, maze, 3)
        
        if ghost_dist <= 2:  # Ghost can reach us in 1-2 moves
            immediate_danger = True
            score -= 1000000  # Must escape immediately
        elif ghost_dist <= 5:
            danger_level = (6 - ghost_dist) ** 3
            score -= danger_level * 1000
            
        # 2. DOT COLLECTION (only when safe)
        if not immediate_danger:
            uneaten_dots = maze.get_uneaten_dots()
            
            # On a dot - absolute priority
            if maze.is_dot_uneaten(*pacman_pos):
                score += 50000
            elif uneaten_dots:
                # Find nearest reachable dot with BFS
                dot_distances = [self.bfs_shortest_path(pacman_pos, dot, maze) for dot in uneaten_dots]
                if dot_distances:
                    dot_dist, dot_path = min(dot_distances, key=lambda x: x[0])
                else:
                    dot_dist, dot_path = float('inf'), []
                
                if dot_dist < float('inf'):
                    # Reward shorter paths more
                    path_bonus = 1000 / (1 + dot_dist)
                    score += path_bonus
                    
                    # Reward clearing clusters
                    nearby_dots = sum(
                        1 for other_dot in uneaten_dots 
                        if self.bfs_shortest_path(dot_path[-1], other_dot, maze)[0] <= 3
                    )
                    score += nearby_dots * 30
                    
                    # Cache the best dot path
                    self.last_dot_path = dot_path[1:] if len(dot_path) > 1 else []

        # 3. PATH SMOOTHNESS (encourage continuous paths)
        if len(self.last_dot_path) > 1 and pacman_pos == self.last_dot_path[0]:
            score += 50  # Bonus for following planned path
            
        # 4. MICRO-OPTIMIZATIONS (ensure unique scores)
        score += (pacman_pos[0] * 31 + pacman_pos[1]) * 0.00001
        
        return score
    def getAction(self, pacman_pos, ghost_pos, maze):
        # Clear cache periodically
        if len(self.path_cache) > 2000:
            self.path_cache.clear()
        if len(self.ghost_danger_cache) > 2000:
            self.ghost_danger_cache.clear()
            
        # 1. Check if we're on a dot - eat it immediately
        if maze.is_dot_uneaten(*pacman_pos):
            return pacman_pos
            
        # 2. Get all possible moves
        possible_moves = []
        for dx, dy in self.moves:
            new_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
            if maze.can_move(*new_pos):
                possible_moves.append(new_pos)
                
        if not possible_moves:
            return pacman_pos
            
        # 3. Check immediate ghost danger
        ghost_dist, _ = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        danger_zones = self.calculate_ghost_danger(ghost_pos, maze, 3)
        
        # 4. If in immediate danger, escape
        if ghost_dist <= 2:
            safe_moves = [m for m in possible_moves if m not in danger_zones]
            if safe_moves:
                # Choose safe move that maximizes distance from ghost
                return max(safe_moves,
                         key=lambda m: self.bfs_shortest_path(m, ghost_pos, maze)[0])
            # If no safe moves, run to farthest position
            return max(possible_moves,
                     key=lambda m: self.bfs_shortest_path(m, ghost_pos, maze)[0])
                     
        # 5. Normal minimax evaluation
        best_score = -float('inf')
        best_move = possible_moves[0]
        
        for move in possible_moves:
            score = self.minimax(move, ghost_pos, maze, self.depth,
                               -float('inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

    def minimax(self, pacman_pos, ghost_pos, maze, depth, alpha, beta, maximizing_player):
        if depth == 0 or maze.all_dots_eaten():
            return self.evaluationFunction(pacman_pos, ghost_pos, maze)
            
        ghost_dist, _ = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        if ghost_dist <= 1:  # Ghost caught us in this path
            return -float('inf') if maximizing_player else float('inf')
            
        if maximizing_player:  # Pacman's turn
            max_eval = -float('inf')
            for dx, dy in self.moves:
                new_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
                if maze.can_move(*new_pos):
                    eval = self.minimax(new_pos, ghost_pos, maze, depth-1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:  # Ghost's turn
            min_eval = float('inf')
            for dx, dy in self.moves:
                new_pos = (ghost_pos[0] + dx, ghost_pos[1] + dy)
                if maze.can_move(*new_pos):
                    eval = self.minimax(pacman_pos, new_pos, maze, depth-1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class Pacman:
    def __init__(self, x, y, maze):
        self.pos = (x, y)
        self.prevPos = (x, y)
        self.maze = maze
        self.all_goals_reached = False
        self.dir = "r"
        self.score = 0
        self.alive = True
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.next_move = None
        self.speed = 2  # Faster than ghost
        self.move_counter = 0
        self.agent = MinimaxAgent(depth=2)

        if self.maze.is_dot_uneaten(x, y):
            self.maze.eat_dot(x, y)
            self.score += 10

    def update(self, ghost_pos):
        # Only update move when we're ready to execute it
        if self.move_counter == 0:
            self.next_move = self.agent.getAction(self.pos, ghost_pos, self.maze)


    def move(self):
        self.move_counter += 1
        if self.move_counter < 1/self.speed:
            return False
            
        self.move_counter = 0
        if self.next_move and self.alive:
            self.prevPos = self.pos
            self.pos = self.next_move
            
            if self.maze.is_dot_uneaten(self.pos[0], self.pos[1]):
                self.maze.eat_dot(self.pos[0], self.pos[1])
                self.score += 10
                
            if self.maze.all_dots_eaten():
                self.all_goals_reached = True
                
            return True
        return False

    def get_direction(self):
        (pos_x, pos_y) = (self.prevPos[0] - self.pos[0], self.prevPos[1] - self.pos[1])
        self.dir = {(-1, 0): 'r', (1, 0): 'l', (0, -1): 'd', (0, 1): 'u'}.get((pos_x, pos_y), self.dir)

    def draw(self, screen):
        if self.alive:
            self.get_direction()
            x = self.pos[0] * TILE_SIZE
            y = self.pos[1] * TILE_SIZE
            pacman_rect = pygame.Rect(x + 2, y + 2, TILE_SIZE - 4, TILE_SIZE - 4)
            pygame.draw.circle(screen, DOT_COLOR, pacman_rect.center, TILE_SIZE // 2 - 2)
        else:
            x, y = self.pos
            center_x = x * TILE_SIZE + TILE_SIZE // 2
            center_y = y * TILE_SIZE + TILE_SIZE // 2
            size = TILE_SIZE // 2 - 2
            pygame.draw.line(screen, DOT_COLOR, (center_x - size, center_y - size),
                           (center_x + size, center_y + size), 2)
            pygame.draw.line(screen, DOT_COLOR, (center_x - size, center_y + size),
                           (center_x + size, center_y - size), 2)

    def get_rect(self):
        return pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman with Minimax (1 Ghost)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 20, bold=True)
        self.maze = Maze()
        self.pacman_start_pos = (10, 1)
        self.ghost_start_pos = (GRID_WIDTH - 2, GRID_HEIGHT - 2)
        self.running = True
        self.game_over = False
        self.ghost = None
        self.start_game()

    def start_game(self):
        self.maze = Maze()
        self.pacman = Pacman(*self.pacman_start_pos, self.maze)
        self.ghost = Ghost(*self.ghost_start_pos, self.maze, self)
        self.start_time = time.time()
        self.end_time = None
        self.game_over = False

    def draw(self):
        self.screen.fill(BLUE)
        self.maze.draw(self.screen)
        self.ghost.draw(self.screen)
        self.pacman.draw(self.screen)

        score_text = f"Score: {self.pacman.score}"
        txt = self.font.render(score_text, True, WHITE)
        self.screen.blit(txt, (10, 10))

        if self.game_over:
            self.end_time = self.end_time or time.time()
            elapsed = round(self.end_time - self.start_time, 2)

            if self.pacman.all_goals_reached:
                result_text = "YOU WIN!"
                result_color = GREEN
            else:
                result_text = "GAME OVER"
                result_color = GOAL_COLOR

            stats = [
                result_text,
                f"Time: {elapsed}s",
                f"Score: {self.pacman.score}",
                f"Dots: {len(self.maze.goals) - len(self.maze.get_uneaten_dots())}/{len(self.maze.goals)}",
                "Press R to Restart or Q to Quit"
            ]

            for i, line in enumerate(stats):
                txt = self.font.render(line, True, result_color if i == 0 else WHITE)
                self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 60 + i * 30))

        pygame.display.flip()

    def check_collision(self):
        pacman_rect = self.pacman.get_rect()
        ghost_rect = self.ghost.get_rect()
        if pacman_rect.colliderect(ghost_rect):
            self.pacman.alive = False
            return True
        return False

    def update(self):
        if self.game_over:
            return

        # Pacman decides move using minimax
        self.pacman.update(self.ghost.pos)
        
        # Ghost moves
        self.ghost.move(self.pacman.pos)
        
        # Pacman executes move
        self.pacman.move()

        # Check collisions and game state
        if self.check_collision() or self.pacman.all_goals_reached:
            self.game_over = True
            self.end_time = time.time()

    def run(self):
        while self.running:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.start_game()
                        elif event.key == pygame.K_q:
                            self.running = False

            if not self.game_over:
                self.update()

            self.draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()