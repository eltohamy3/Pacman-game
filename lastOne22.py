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

class MinimaxAgent:
    def __init__(self, depth=3):
        self.depth = depth
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.last_positions = deque(maxlen=10)  # Longer memory for cycling detection
        self.last_move = None
    def apply_tiebreakers(self, moves, pacman_pos, ghost_pos, maze):
        """Hierarchical tiebreaking system"""
        # Stage 1: Directional consistency
        if self.last_move:
            consistent_moves = [
                move for move in moves
                if (move[0]-pacman_pos[0], move[1]-pacman_pos[1]) == self.last_move
            ]
            if consistent_moves:
                return consistent_moves
        
        # Stage 2: Dot proximity
        uneaten_dots = maze.get_uneaten_dots()
        if uneaten_dots:
            nearest_dot = min(uneaten_dots, key=lambda d: manhattan_distance(pacman_pos, d))
            dot_distances = [
                (manhattan_distance(move, nearest_dot), move)
                for move in moves
            ]
            min_dist = min(dot_distances)[0]
            return [move for dist, move in dot_distances if dist == min_dist]
        
        # Stage 3: Ghost avoidance
        ghost_distances = [
            (manhattan_distance(move, ghost_pos), move)
            for move in moves
        ]
        max_dist = max(ghost_distances)[0]
        return [move for dist, move in ghost_distances if dist == max_dist]

    def evaluationFunction(self, pacman_pos, ghost_pos, maze):
        """
        Ultimate evaluation function with guaranteed decision-making
        Returns a float score where equality is virtually impossible
        """
        score = 0.0  # Using float for more granular scores
        pac_x, pac_y = pacman_pos
        ghost_x, ghost_y = ghost_pos
        uneaten_dots = maze.get_uneaten_dots()
        num_dots = len(uneaten_dots)
        
        # 1. Primary Objectives (large weights)
        # -------------------------------------
        # Immediate dot collection
        if maze.is_dot_uneaten(pac_x, pac_y):
            score += 500 * (1 + num_dots/len(maze.goals))  # Scaling reward
        
        # Nearest dot distance (inverse exponential)
        if uneaten_dots:
            nearest_dot = min(uneaten_dots, key=lambda d: manhattan_distance(pacman_pos, d))
            dist = manhattan_distance(pacman_pos, nearest_dot)
            score += 100 * math.exp(-0.5 * dist)  # Rapidly decreasing reward
        
        # 2. Ghost Avoidance (dynamic weights)
        # ------------------------------------
        ghost_dist = manhattan_distance(pacman_pos, ghost_pos)
        
        # Danger zones (non-linear)
        if ghost_dist < 8:
            danger = (9 - ghost_dist) ** 2.5  # Sharp increase
            score -= 25 * danger
            
            # Directional danger
            if (pac_x == ghost_x or pac_y == ghost_y) and ghost_dist < 5:
                score -= 50 * danger
        
        # 3. Strategic Positioning (medium weights)
        # ----------------------------------------
        # Center control bonus
        center_x, center_y = GRID_WIDTH/2, GRID_HEIGHT/2
        center_dist = math.sqrt((pac_x-center_x)**2 + (pac_y-center_y)**2)
        score += 30/(1 + center_dist)
        
        # Mobility bonus
        valid_moves = sum(1 for dx, dy in self.moves if maze.can_move(pac_x+dx, pac_y+dy))
        score += 10 * valid_moves
        
        # 4. Anti-Cycling Mechanisms (small weights)
        # ------------------------------------------
        # Recent position penalty
        for i, pos in enumerate(reversed(self.last_positions)):
            if pos == pacman_pos:
                score -= 30/(i+1)  # Decaying penalty
        
        # Direction change penalty
        if self.last_move and len(self.last_positions) >= 2:
            prev_move = self.last_move
            current_move = (pac_x - self.last_positions[-1][0], 
                          pac_y - self.last_positions[-1][1])
            if prev_move != current_move:
                score -= 15
        
        # 5. Micro-Optimizations (tiny weights)
        # -------------------------------------
        # Position-based hash (unique per cell)
        position_hash = (pac_x * 31 + pac_y) / 1000  # 0-1 scaled
        score += position_hash * 0.001
        
        # Dot density in 5x5 area
        nearby_dots = sum(1 for x,y in uneaten_dots 
                         if abs(x-pac_x) <= 2 and abs(y-pac_y) <= 2)
        score += nearby_dots * 0.1
        
        return score
    def find_nearest_dot(self, pos, maze):
        uneaten_dots = maze.get_uneaten_dots()
        if not uneaten_dots:
            return None
            
        return min(uneaten_dots, key=lambda dot: manhattan_distance(pos, dot))
    
    def minimax(self, pacman_pos, ghost_pos, maze, depth, alpha, beta, maximizing_player):
        if depth == 0 or maze.all_dots_eaten() or manhattan_distance(pacman_pos, ghost_pos) < 1:
            return self.evaluationFunction(pacman_pos, ghost_pos, maze)
            
        if maximizing_player:  # Pacman's turn (maximize)
            max_eval = -float('inf')
            for dx, dy in self.moves:
                new_x, new_y = pacman_pos[0] + dx, pacman_pos[1] + dy
                if maze.can_move(new_x, new_y):
                    eval = self.minimax((new_x, new_y), ghost_pos, maze, depth-1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta pruning
            return max_eval
        else:  # Ghost's turn (minimize)
            min_eval = float('inf')
            for dx, dy in self.moves:
                new_x, new_y = ghost_pos[0] + dx, ghost_pos[1] + dy
                if maze.can_move(new_x, new_y):
                    eval = self.minimax(pacman_pos, (new_x, new_y), maze, depth-1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha pruning
            return min_eval
    
    def getAction(self, pacman_pos, ghost_pos, maze):
        self.last_positions.append(pacman_pos)
        
        # Generate all valid moves
        possible_moves = []
        for dx, dy in self.moves:
            new_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
            if maze.can_move(*new_pos):
                possible_moves.append(new_pos)
        
        if not possible_moves:
            return pacman_pos  # No valid moves
        
        # Evaluate all moves with minimax
        scored_moves = []
        for move in possible_moves:
            score = self.minimax(move, ghost_pos, maze, self.depth,
                               -float('inf'), float('inf'), False)
            scored_moves.append((score, move))
        
        # Find all moves with maximum score
        max_score = max(scored_moves, key=lambda x: x[0])[0]
        best_moves = [move for score, move in scored_moves if abs(score - max_score) < 1e-6]
        
        # Apply tiebreakers if needed
        if len(best_moves) > 1:
            best_moves = self.apply_tiebreakers(best_moves, pacman_pos, ghost_pos, maze)
        
        # Update last move direction
        chosen_move = best_moves[0]
        self.last_move = (chosen_move[0] - pacman_pos[0], 
                         chosen_move[1] - pacman_pos[1])
        
        return chosen_move
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