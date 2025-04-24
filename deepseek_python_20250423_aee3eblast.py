import pygame
import math
import random
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
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 139)

# Maze layout
BIGSEARCH = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,0,0,0,1,1,1,0,0,0,1],
    [1,1,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,1,1],
    [1,0,0,0,1,0,1,1,1,0,1,0,1,1,1,2,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1],
    [1,0,1,1,1,0,0,0,0,0,0,0,1,2,2,2,2,2,1,0,0,0,0,0,0,0,1,1,1,0,1],
    [1,0,0,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,0,0,1],
    [1,1,1,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,1,1],
    [1,0,0,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,1,0,1,0,1,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Maze:
    def __init__(self):
        self.layout = BIGSEARCH
        self.goals = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] in [0, 2]:
                    self.goals.append((x, y))
        self.reset()

    def reset(self):
        self.uneaten = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for x, y in self.goals:
            self.uneaten[y][x] = True

    def can_move(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.layout[y][x] in [0, 2]

    def eat_dot(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.uneaten[y][x] = False

    def is_dot_uneaten(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and self.uneaten[y][x]

    def get_uneaten_dots(self):
        return {(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH) if self.is_dot_uneaten(x, y)}

    def all_dots_eaten(self):
        return len(self.get_uneaten_dots()) == 0

    def draw(self, screen):
        # Draw walls and background
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.layout[y][x] == 1:
                    pygame.draw.rect(screen, DARK_BLUE, rect)
                else:
                    pygame.draw.rect(screen, BLACK, rect)
        
        # Draw dots
        for x, y in self.get_uneaten_dots():
            center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.circle(screen, YELLOW, center, 4)

class MinimaxAgent:
    def __init__(self, depth=5):
        self.depth = depth
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.path_cache = {}
        self.ghost_danger_cache = {}
        self.last_dot_path = []
        self.safety_threshold = 4
        self.visited_positions = dict()
        self.last_dot_time = time.time()
        self.dot_check_interval = 2.0
        self.prevPos = None
        self.last_new_area_time = time.time()
        self.position_history = deque(maxlen=10)
        self.state_hash_seed = random.randint(1, 10000)
        self.dot_value = 50000  # Increased pellet value
        self.ghost_danger_zone = 5
        self.dot_cluster_bonus = 1.5  # Bonus for pellet clusters

    def get_state_hash(self, pacman_pos, ghost_pos):
        return (pacman_pos[0] * 3571 + pacman_pos[1] * 6421 + 
               ghost_pos[0] * 9973 + ghost_pos[1] * 7919) ^ self.state_hash_seed

    def evaluate_state(self, pacman_pos, ghost_pos, maze):
        state_hash = self.get_state_hash(pacman_pos, ghost_pos)
        score = 0.0
        uneaten_dots = maze.get_uneaten_dots()
        num_dots = len(uneaten_dots)
        
        # Immediate loss if on ghost
        if pacman_pos == ghost_pos:
            return -float('inf')
        
        # Strong penalty for being adjacent to ghost
        is_adjacent_to_ghost = False
        for dx, dy in self.moves:
            neighbor_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
            if neighbor_pos == ghost_pos:
                is_adjacent_to_ghost = True
                break
        
        if is_adjacent_to_ghost:
            score -= 100000  # Massive penalty for adjacent positions
        
        # Pellet collection with hash-based variations
        if maze.is_dot_uneaten(*pacman_pos):
            base = self.dot_value + (state_hash % 100)
            walls = sum(1 for dx, dy in self.moves 
                    if not maze.can_move(pacman_pos[0]+dx, pacman_pos[1]+dy))
            score += base * (1 + walls/2)
            if num_dots <= 5:  # Increased end-game bonus
                score += (self.dot_value//2 + (state_hash % 50)) * (6 - num_dots)
        
        # Ghost danger evaluation
        ghost_dist, ghost_path = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        if ghost_dist <= 2:
            return -float('inf') * (1 + (state_hash % 10) * 0.01)
        elif ghost_dist <= self.ghost_danger_zone:
            danger = (self.ghost_danger_zone - ghost_dist) ** 3 * (1 + (state_hash % 20) * 0.005)
            score -= danger * 10000
        
        # Strategic pellet pathing
        if ghost_dist > 3 and uneaten_dots:
            dot_scores = []
            for dot in uneaten_dots:
                dist, path = self.bfs_shortest_path(pacman_pos, dot, maze)
                if dist < float('inf'):
                    density = self.calculate_dot_density(dot, maze, radius=3)
                    dot_hash = dot[0] * 123 + dot[1] * 321
                    path_safety = self.assess_path_safety(path, ghost_pos, maze)
                    
                    dot_score = (self.dot_value / (1 + dist)) * \
                            (1 + density * 0.3) * \
                            (1 + (dot_hash % 20) * 0.001) * \
                            path_safety * \
                            self.dot_cluster_bonus
                    
                    # Penalize paths that go near ghosts
                    if any(pos == ghost_pos for pos in path):
                        dot_score *= 0.1  # Reduce score by 90% if path goes through ghost
                    
                    dot_scores.append((dot_score, path))
            
            if dot_scores:
                best_score, best_path = max(dot_scores, key=lambda x: x[0])
                score += best_score
                self.last_dot_path = best_path[1:] if len(best_path) > 1 else []

        # Exploration management with hash-based variations
        visit_count = self.visited_positions.get(pacman_pos, 0)
        score -= visit_count * 30 * (1 + (state_hash % 5) * 0.01)
        
        if pacman_pos not in self.visited_positions:
            score += 150 * (1 + (state_hash % 10) * 0.01)
            if time.time() - self.last_new_area_time > 10:
                score += 300 * (1 + (state_hash % 5) * 0.01)
        
        # Movement consistency with hash-based variations
        if self.prevPos:
            current_dir = (pacman_pos[0]-self.prevPos[0], pacman_pos[1]-self.prevPos[1])
            if current_dir in self.moves:
                dir_hash = current_dir[0] * 11 + current_dir[1] * 13
                score += 25 * (1 + (dir_hash % 10) * 0.01)
        
        # Hash-based noise to break ties
        score += (state_hash % 1000) * 0.001
        score += (time.time() % 0.1) * 0.0001
        
        return score

    def assess_path_safety(self, path, ghost_pos, maze):
        min_safety = 1.0
        for pos in path:
            dist, _ = self.bfs_shortest_path(pos, ghost_pos, maze)
            if dist <= 2:
                return 0.01  # Extremely dangerous
            elif dist <= 4:
                min_safety = min(min_safety, 0.5)  # Moderately dangerous
        return min_safety

    def getAction(self, pacman_pos, ghost_pos, maze):
        # First check for emergency ghost avoidance
        for dx, dy in self.moves:
            if (pacman_pos[0] + dx, pacman_pos[1] + dy) == ghost_pos:
                # Find the safest escape move
                escape_moves = []
                for ex, ey in self.moves:
                    new_pos = (pacman_pos[0] + ex, pacman_pos[1] + ey)
                    if maze.can_move(*new_pos) and new_pos != ghost_pos:
                        dist = abs(new_pos[0] - ghost_pos[0]) + abs(new_pos[1] - ghost_pos[1])
                        escape_moves.append((dist, new_pos))
                if escape_moves:
                    return max(escape_moves, key=lambda x: x[0])[1]
                return pacman_pos  # If no escape, stay put

        self.position_history.append(pacman_pos)
        self.visited_positions[pacman_pos] = self.visited_positions.get(pacman_pos, 0) + 1
        
        # Always eat pellet if on one
        if maze.is_dot_uneaten(*pacman_pos):
            self.prevPos = pacman_pos
            return pacman_pos
            
        possible_moves = []
        for dx, dy in self.moves:
            new_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
            if maze.can_move(*new_pos) and new_pos != ghost_pos:
                possible_moves.append(new_pos)
        
        if not possible_moves:
            self.prevPos = pacman_pos
            return pacman_pos
            
        # Emergency ghost avoidance
        ghost_dist, _ = self.bfs_shortest_path(pacman_pos, ghost_pos, maze)
        if ghost_dist <= 3:
            escape_moves = []
            for move in possible_moves:
                new_dist, _ = self.bfs_shortest_path(move, ghost_pos, maze)
                escape_moves.append((new_dist, move))
            self.prevPos = pacman_pos
            return max(escape_moves, key=lambda x: x[0])[1]
        
        # Normal operation - maximize pellet collection
        best_score = -float('inf')
        best_move = possible_moves[0]
        
        for move in possible_moves:
            # Immediate pellet check
            move_score = 0
            if maze.is_dot_uneaten(*move):
                move_score += self.dot_value * 1.5  # Bonus for immediate pellets
            
            # Future evaluation
            eval_score = self.minimax(move, ghost_pos, maze, self.depth-1, -float('inf'), float('inf'), False)
            total_score = move_score + eval_score
            
            if total_score > best_score:
                best_score = total_score
                best_move = move
        
        self.prevPos = pacman_pos
        return best_move

    def minimax(self, pacman_pos, ghost_pos, maze, depth, alpha, beta, is_pacman_turn):
        if depth == 0 or maze.all_dots_eaten():
            return self.evaluate_state(pacman_pos, ghost_pos, maze)
            
        if is_pacman_turn:
            max_score = -float('inf')
            for dx, dy in self.moves:
                new_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
                if maze.can_move(*new_pos):
                    score = self.minimax(new_pos, ghost_pos, maze, depth-1, alpha, beta, False)
                    max_score = max(max_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return max_score
        else:
            min_score = float('inf')
            for dx, dy in self.moves:
                new_pos = (ghost_pos[0] + dx, ghost_pos[1] + dy)
                if maze.can_move(*new_pos):
                    score = self.minimax(pacman_pos, new_pos, maze, depth-1, alpha, beta, True)
                    min_score = min(min_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return min_score

    def bfs_shortest_path(self, start, target, maze):
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
                if maze.can_move(*new_pos):
                    if new_pos == target:
                        result = (len(path), path + [new_pos])
                        self.path_cache[cache_key] = result
                        return result
                    if new_pos not in visited:
                        visited.add(new_pos)
                        queue.append((new_pos, path + [new_pos]))
        
        return float('inf'), []

    def calculate_dot_density(self, pos, maze, radius):
        x, y = pos
        count = 0
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and maze.is_dot_uneaten(nx, ny):
                    count += 1
        return count

    def assess_path_safety(self, path, ghost_pos, maze):
        min_safety = 1.0
        for pos in path:
            dist, _ = self.bfs_shortest_path(pos, ghost_pos, maze)
            if dist <= 3:
                return 0.1  # Extremely dangerous
            elif dist <= 5:
                min_safety = min(min_safety, 0.5)  # Moderately dangerous
        return min_safety

class Ghost:
    def __init__(self, x, y, maze, game):
        self.pos = (x, y)
        self.maze = maze
        self.game = game
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.path = []
        self.speed = 1
        self.move_counter = 0

    def find_path_to_pacman(self, target_pos):
        queue = deque([(self.pos, [])])
        visited = set()
        
        while queue:
            pos, path = queue.popleft()
            if pos == target_pos:
                self.path = path
                return
                
            for dx, dy in self.moves:
                new_pos = (pos[0] + dx, pos[1] + dy)
                if self.maze.can_move(*new_pos) and new_pos not in visited:
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
        self.path = []

    def move(self, pacman_pos):
        self.move_counter += 1
        if self.move_counter < 1/self.speed:
            return False
            
        self.move_counter = 0
        self.find_path_to_pacman(pacman_pos)
        if self.path:
            self.pos = self.path[0]
            return True
        return False

    def draw(self, screen):
        x, y = self.pos
        ghost_rect = pygame.Rect(x * TILE_SIZE + 2, y * TILE_SIZE + 2, TILE_SIZE - 4, TILE_SIZE - 4)
        pygame.draw.rect(screen, RED, ghost_rect)
        pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + 7, y * TILE_SIZE + 7), 3)
        pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE - 7, y * TILE_SIZE + 7), 3)

    def get_rect(self):
        return pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)

class Pacman:
    def __init__(self, x, y, maze):
        self.pos = (x, y)
        self.maze = maze
        self.score = 0
        self.alive = True
        self.next_move = None
        self.speed = 1
        self.move_counter = 0
        self.agent = MinimaxAgent(depth=4)
        
        if self.maze.is_dot_uneaten(x, y):
            self.maze.eat_dot(x, y)
            self.score += 10

    def update(self, ghost_pos):
        self.next_move = self.agent.getAction(self.pos, ghost_pos, self.maze)
        # Emergency collision prevention
        if self.next_move == ghost_pos:
            for dx, dy in self.agent.moves:
                new_pos = (self.pos[0] + dx, self.pos[1] + dy)
                if self.maze.can_move(*new_pos) and new_pos != ghost_pos:
                    self.next_move = new_pos
                    break

    def move(self, ghost_pos):
        self.move_counter += 1
        if self.move_counter < 1/self.speed:
            return False
            
        self.move_counter = 0
        if self.next_move and self.alive:
            # Final safety check
            if self.next_move == ghost_pos:
                return False
                
            self.pos = self.next_move
            
            if self.maze.is_dot_uneaten(*self.pos):
                self.maze.eat_dot(*self.pos)
                self.score += 10
                
            if self.maze.all_dots_eaten():
                return True
        return False

    def draw(self, screen):
        x, y = self.pos
        center = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
        if self.alive:
            pygame.draw.circle(screen, YELLOW, center, TILE_SIZE // 2 - 2)
        else:
            size = TILE_SIZE // 2 - 2
            pygame.draw.line(screen, RED, (center[0] - size, center[1] - size),
                           (center[0] + size, center[1] + size), 2)
            pygame.draw.line(screen, RED, (center[0] - size, center[1] + size),
                           (center[0] + size, center[1] - size), 2)

    def get_rect(self):
        return pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Advanced Pacman AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.reset_game()

    def reset_game(self):
        self.maze = Maze()
        self.pacman = Pacman(15, 7, self.maze)
        self.ghost = Ghost(15, 10, self.maze, self)
        self.start_time = time.time()
        self.game_over = False
        self.win = False

    def draw(self):
        self.screen.fill(BLUE)
        self.maze.draw(self.screen)
        self.ghost.draw(self.screen)
        self.pacman.draw(self.screen)
        
        # Score display
        score_text = f"Score: {self.pacman.score}"
        self.screen.blit(self.font.render(score_text, True, WHITE), (10, 10))
        
        # Game over display
        if self.game_over:
            result = "YOU WIN!" if self.win else "GAME OVER"
            color = GREEN if self.win else RED
            texts = [
                result,
                f"Score: {self.pacman.score}",
                "Press R to restart",
                "Press Q to quit"
            ]
            for i, text in enumerate(texts):
                y_pos = HEIGHT//2 - 30 + i*30
                self.screen.blit(self.font.render(text, True, color if i==0 else WHITE), 
                                (WIDTH//2 - 50, y_pos))
        
        pygame.display.flip()

    def update(self):
        if self.game_over:
            return
            
        self.pacman.update(self.ghost.pos)
        self.ghost.move(self.pacman.pos)
        
        if self.pacman.move(self.ghost.pos):
            self.game_over = True
            self.win = True
            
        if self.pacman.get_rect().colliderect(self.ghost.get_rect()):
            self.pacman.alive = False
            self.game_over = True

    def run(self):
        running = True
        while running:
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_q:
                            running = False
            
            if not self.game_over:
                self.update()
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()