import math
import random
import pygame
import time
from collections import deque
from configuration import *

# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
TILE_SIZE = 21
GRID_WIDTH, GRID_HEIGHT = 31, 15
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH + 10, TILE_SIZE * GRID_HEIGHT + 10

# Maze layout
BIGSEARCH = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
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
                if self.layout[y][x] == 0 or self.layout[y][x] == 2:
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
        self.speed = 0.9  # Slower than Pacman
        self.move_counter = 0

    def find_path_to_pacman(self, pacman_pos):
        queue = deque([(self.pos, [])])
        visited = set()
        
        while queue:
            current, path = queue.popleft()
            if current == pacman_pos:
                self.path = path
                return
                
            for dx, dy in self.moves:
                nx, ny = current[0] + dx, current[1] + dy
                if self.maze.can_move(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        self.path = []

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
        x = self.pos[0] * TILE_SIZE
        y = self.pos[1] * TILE_SIZE
        ghost_img = pygame.image.load(blinky_ghost)
        ghost_img = pygame.transform.scale(ghost_img, (TILE_SIZE, TILE_SIZE))
        screen.blit(ghost_img, (x, y))

    def get_rect(self):
        return pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)

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
        self.speed = 1.2  # Faster than ghost
        self.move_counter = 0
        self.last_dot_time = time.time()
        self.dot_check_interval = 2  # Check for nearest dot every 2 seconds
        self.frame_idx = 0

        if self.maze.is_dot_uneaten(x, y):
            self.maze.eat_dot(x, y)
            self.score += 10

    def find_nearest_dot(self):
        uneaten_dots = self.maze.get_uneaten_dots()
        if not uneaten_dots:
            return None
            
        # Find the nearest dot using BFS
        queue = deque([(self.pos, [])])
        visited = set()
        
        while queue:
            current, path = queue.popleft()
            if current in uneaten_dots:
                return path[0] if path else current
                
            for dx, dy in self.moves:
                nx, ny = current[0] + dx, current[1] + dy
                if self.maze.can_move(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return None

    def evaluate_state(self, pacman_pos, ghost_pos):
        """Evaluation function for leaf nodes"""
        score = 0
        
        # Reward for eating dots
        if self.maze.is_dot_uneaten(pacman_pos[0], pacman_pos[1]):
            score += 100
        
        # Distance to nearest dot
        nearest_dot = self.find_nearest_dot()
        if nearest_dot:
            dot_dist = abs(pacman_pos[0] - nearest_dot[0]) + abs(pacman_pos[1] - nearest_dot[1])
            score -= dot_dist * 2
        
        # Ghost proximity
        ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
        if ghost_dist < 4:
            score -= (100 - ghost_dist * 20)
            if ghost_dist < 2:
                score -= 200  # Very big penalty if ghost is very close
        
        return score

    def minimax(self, pacman_pos, ghost_pos, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
        """
        Minimax algorithm with alpha-beta pruning
        - maximizing_player: True for Pacman's turn, False for ghost's turn
        - depth: current depth in the tree
        """
        # Base case: leaf node or terminal state
        if depth == 0 or self.is_terminal_state(pacman_pos, ghost_pos):
            return self.evaluate_state(pacman_pos, ghost_pos), pacman_pos
        
        if maximizing_player:  # Pacman's turn
            max_eval = -math.inf
            best_move = pacman_pos
            
            for dx, dy in self.moves:
                nx, ny = pacman_pos[0] + dx, pacman_pos[1] + dy
                if self.maze.can_move(nx, ny) and (nx,ny) !=ghost_pos :
                    eval, _ = self.minimax((nx, ny), ghost_pos, depth-1, False, alpha, beta)
                    
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (nx, ny)
                    
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cutoff
            
            return max_eval, best_move
        else:  # Ghost's turn (minimizing player)
            min_eval = math.inf
            best_move = ghost_pos
            
            for dx, dy in self.moves:
                nx, ny = ghost_pos[0] + dx, ghost_pos[1] + dy
                if self.maze.can_move(nx, ny):
                    eval, _ = self.minimax(pacman_pos, (nx, ny), depth-1, True, alpha, beta)
                    
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (nx, ny)
                    
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cutoff
            
            return min_eval, best_move

    def is_terminal_state(self, pacman_pos, ghost_pos):
        """Check if the state is terminal (game over)"""
        # Check if pacman caught by ghost
        if pacman_pos == ghost_pos:
            return True
        
        # Check if all dots eaten
        if len(self.maze.get_uneaten_dots()) == 0:
            return True
            
        return False

    def minimax_decision(self, ghost_pos, depth=2):
        """Make decision using minimax with specified depth"""
        _, best_move = self.minimax(self.pos, ghost_pos, depth, True)
        return best_move

    def update(self, ghost_pos):
        # Periodically check for nearest dot to prevent getting stuck
        if time.time() - self.last_dot_time > self.dot_check_interval:
            nearest_dot = self.find_nearest_dot()
            if nearest_dot:
                self.next_move = nearest_dot
            self.last_dot_time = time.time()
        else:
            # Use minimax with depth 2
            self.next_move = self.minimax_decision(ghost_pos, depth=2)

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

    def get_direction ( self , screen ) :
        (pos_x , pos_y) = (self.prevPos [0] - self.pos [0] , self.prevPos [1] - self.pos [1])
        self.dir = movement_direction.get ( (pos_x , pos_y) )

    def update_frame ( self , screen ) :
        x = self.pos [0] * TILE_SIZE
        y = self.pos [1] * TILE_SIZE

        pacman_dir = pacman_directions.get ( self.dir )
        self.frame_idx = self.frame_idx % len ( pacman_dir )

        pacman_img = pygame.image.load ( pacman_dir [self.frame_idx] )
        pacman_img = pygame.transform.scale ( pacman_img , (TILE_SIZE , TILE_SIZE) )
        screen.blit ( pacman_img , (x , y) )

        if not self.all_goals_reached:
            self.frame_idx += 1

    def draw(self, screen):
        self.get_direction(screen)
        self.update_frame(screen)

    def get_rect(self):
        return pygame.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pacman with Minimax (Depth 2)")
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

        # Pacman decides move
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