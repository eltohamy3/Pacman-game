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
import math
from collections import deque
import time

import math
from collections import deque
import time
import random

class MinimaxAgent:
    def __init__(self, depth=3):
        self.depth = depth
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.path_cache = {}
        self.ghost_danger_cache = {}
        self.last_dot_path = []
        self.safety_threshold = 4
        self.visited_positions = dict()  # Track positions and visit counts
        self.last_dot_time = time.time()
        self.dot_check_interval = 2.0
        self.prevPos = None
        self.last_new_area_time = time.time()
        self.position_history = deque(maxlen=10)  # Track recent positions
        self.state_hash_seed = random.randint(1, 10000)  # Unique seed per game

    def get_state_hash(self, pacman_pos, ghost_pos):
        """Create unique hash for game state"""
        return (pacman_pos[0] * 3571 + pacman_pos[1] * 6421 + 
               ghost_pos[0] * 9973 + ghost_pos[1] * 7919) ^ self.state_hash_seed

    def evaluate_state(self, pacman_pos, ghost_pos, maze):
        """Completely unique state evaluation with no repeats"""
        state_hash = self.get_state_hash(pacman_pos, ghost_pos)
        score = 0.0
        uneaten_dots = maze.get_uneaten_dots()
        num_dots = len(uneaten_dots)
        
        # 1. Immediate Dot Consumption (unique bonus)
        if maze.is_dot_uneaten(*pacman_pos):
            base = 10000 + (state_hash % 100)  # Add unique variation
            walls = sum(1 for dx, dy in self.moves 
                       if not maze.can_move(pacman_pos[0]+dx, pacman_pos[1]+dy))
            score += base * (1 + walls/2)
            if num_dots <= 3:
                score += (5000 + (state_hash % 50)) * (4 - num_dots)
        
        # 2. Ghost Threat (dynamic danger scaling)
        ghost_dist, ghost_path = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        if ghost_dist <= 2:
            return -float('inf') * (1 + (state_hash % 10) * 0.01)  # Unique penalty
        elif ghost_dist <= 5:
            danger = (6 - ghost_dist) ** 3 * (1 + (state_hash % 20) * 0.005)
            score -= danger * 5000
        
        # 3. Dot Collection (unique path scoring)
        if ghost_dist > 3 and uneaten_dots:
            dot_scores = []
            for dot in uneaten_dots:
                dist, path = self.bfs_shortest_path(pacman_pos, dot, maze)
                if dist < float('inf'):
                    density = self.calculate_dot_density(dot, maze)
                    dot_hash = dot[0] * 123 + dot[1] * 321
                    dot_score = (5000 / (1 + dist)) * (1 + density * 0.2) * (1 + (dot_hash % 20) * 0.001)
                    dot_scores.append((dot_score, path))
            
            if dot_scores:
                best_score, best_path = max(dot_scores, key=lambda x: x[0])
                score += best_score
                self.last_dot_path = best_path[1:] if len(best_path) > 1 else []

        # 4. Position History (anti-repetition)
        visit_count = self.visited_positions.get(pacman_pos, 0)
        score -= visit_count * 50  # Penalize revisited positions
        if pacman_pos not in self.visited_positions:
            score += 100 * (1 + (state_hash % 10) * 0.01)
            if time.time() - self.last_new_area_time > 10:
                score += 200 * (1 + (state_hash % 5) * 0.01)
        
        # 5. Movement Patterns (unique direction bonus)
        if self.prevPos:
            current_dir = (pacman_pos[0]-self.prevPos[0], pacman_pos[1]-self.prevPos[1])
            if current_dir in self.moves:
                dir_hash = current_dir[0] * 11 + current_dir[1] * 13
                score += 20 * (1 + (dir_hash % 10) * 0.01)
        
        # 6. Micro-Optimizations (guaranteed uniqueness)
        score += (state_hash % 1000) * 0.001
        score += (time.time() % 0.1) * 0.0001
        
        return score

    def getAction(self, pacman_pos, ghost_pos, maze):
        # Update position history
        self.position_history.append(pacman_pos)
        self.visited_positions[pacman_pos] = self.visited_positions.get(pacman_pos, 0) + 1
        
        if pacman_pos not in self.visited_positions:
            self.last_new_area_time = time.time()
        
        # Immediate dot consumption
        if maze.is_dot_uneaten(*pacman_pos):
            self.prevPos = pacman_pos
            return pacman_pos
            
        # Get possible moves
        possible_moves = []
        for dx, dy in self.moves:
            new_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
            if maze.can_move(*new_pos):
                possible_moves.append(new_pos)
        
        if not possible_moves:
            self.prevPos = pacman_pos
            return pacman_pos
            
        # Check immediate ghost danger
        ghost_dist, _ = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        if ghost_dist <= 2:
            # Find safest escape move
            escape_moves = []
            for move in possible_moves:
                new_dist, _ = self.bfs_shortest_path(move, ghost_pos, maze)
                escape_moves.append((new_dist, move))
            self.prevPos = pacman_pos
            return max(escape_moves, key=lambda x: x[0])[1]
        
        # Use minimax with limited depth
        best_score = -float('inf')
        best_move = possible_moves[0]
        
        for move in possible_moves:
            score = self.minimax(move, ghost_pos, maze, self.depth - 1, -float('inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move
        
        self.prevPos = pacman_pos
        return best_move

    def minimax(self, pacman_pos, ghost_pos, maze, depth, alpha, beta, maximizing_player):
        """Minimax with alpha-beta pruning"""
        if depth == 0 or maze.all_dots_eaten():
            return self.evaluate_state(pacman_pos, ghost_pos, maze)
            
        ghost_dist, _ = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        if ghost_dist <= 1:
            return -float('inf') if maximizing_player else float('inf')
            
        if maximizing_player:  # Pacman's turn
            max_eval = -float('inf')
            for dx, dy in self.moves:
                new_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
                if maze.can_move(*new_pos):
                    eval = self.minimax(new_pos, ghost_pos, maze, depth - 1, alpha, beta, False)
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
                    eval = self.minimax(pacman_pos, new_pos, maze, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def bfs_shortest_path(self, start, target, maze):
        """BFS pathfinding with wall collision detection"""
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
                if not maze.can_move(*new_pos):  # Wall check
                    continue
                if new_pos == target:
                    result = (len(path), path + [new_pos])
                    self.path_cache[cache_key] = result
                    return result
                if new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
        
        return float('inf'), []  # No path found

    def calculate_dot_density(self, pos, maze, radius=2):
        """Count dots in surrounding area"""
        x, y = pos
        min_x = max(0, x - radius)
        max_x = min(GRID_WIDTH - 1, x + radius)
        min_y = max(0, y - radius)
        max_y = min(GRID_HEIGHT - 1, y + radius)
        
        return sum(1 for dot_x, dot_y in maze.get_uneaten_dots()
                 if min_x <= dot_x <= max_x and min_y <= dot_y <= max_y)
        

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
        self.speed = 3  # Increased from 2 (original value)
        self.move_counter = 0
        self.speed_boost_time = 0  # For temporary speed boosts

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
        # Original: if self.move_counter < 1/self.speed:
        if self.move_counter < max(0.1, 1/self.speed):  # Minimum 0.1 seconds between moves
            return False
            
        self.move_counter = 0
        if self.next_move and self.alive:
            self.prevPos = self.pos
            self.pos = self.next_move
            
            if self.maze.is_dot_uneaten(self.pos[0], self.pos[1]):
                self.maze.eat_dot(self.pos[0], self.pos[1])
                self.score += 10
                # Temporary speed boost when eating dots
                self.speed_boost_time = time.time() + 2  # 2 second boost
                
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