import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 40
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Game Objects
class GameState:
    def __init__(self, pacman_pos, ghost_pos, food, score):
        self.pacman_pos = pacman_pos
        self.ghost_pos = ghost_pos
        self.food = food
        self.score = score

    def generate_successor(self, agent, action):
        new_pos = list(self.pacman_pos if agent == 0 else self.ghost_pos)
        if action == 'UP': new_pos[1] -= 1
        if action == 'DOWN': new_pos[1] += 1
        if action == 'LEFT': new_pos[0] -= 1
        if action == 'RIGHT': new_pos[0] += 1

        new_food = self.food.copy()
        new_score = self.score
        if agent == 0 and new_pos in new_food:
            new_food.remove(tuple(new_pos))
            new_score += 10

        return GameState(
            tuple(new_pos) if agent == 0 else self.pacman_pos,
            tuple(new_pos) if agent == 1 else self.ghost_pos,
            new_food,
            new_score
        )

    def get_legal_actions(self, pos):
        actions = []
        x, y = pos
        if y > 0: actions.append('UP')
        if y < ROWS - 1: actions.append('DOWN')
        if x > 0: actions.append('LEFT')
        if x < COLS - 1: actions.append('RIGHT')
        return actions

    def is_win(self):
        return len(self.food) == 0

    def is_lose(self):
        return self.pacman_pos == self.ghost_pos

def evaluation_function(state):
    pac = state.pacman_pos
    ghost = state.ghost_pos
    if state.is_lose():
        return -9999
    if state.is_win():
        return 9999

    food_dist = [abs(pac[0]-f[0]) + abs(pac[1]-f[1]) for f in state.food]
    closest_food = min(food_dist) if food_dist else 0
    ghost_distance = abs(pac[0] - ghost[0]) + abs(pac[1] - ghost[1])
    return state.score + ghost_distance - closest_food

def minimax(state, depth, agent):
    if depth == 0 or state.is_win() or state.is_lose():
        return evaluation_function(state), None

    if agent == 0:  # Pacman (Max)
        max_score = float('-inf')
        best_action = None
        for action in state.get_legal_actions(state.pacman_pos):
            succ = state.generate_successor(agent, action)
            score, _ = minimax(succ, depth, 1)
            if score > max_score:
                max_score = score
                best_action = action
        return max_score, best_action

    else:  # Ghost (Min)
        min_score = float('inf')
        best_action = None
        for action in state.get_legal_actions(state.ghost_pos):
            succ = state.generate_successor(agent, action)
            score, _ = minimax(succ, depth-1, 0)
            if score < min_score:
                min_score = score
                best_action = action
        return min_score, best_action

def expectimax(state, depth, agent):
    if depth == 0 or state.is_win() or state.is_lose():
        return evaluation_function(state), None

    if agent == 0:  # Pacman (Max)
        max_score = float('-inf')
        best_action = None
        for action in state.get_legal_actions(state.pacman_pos):
            succ = state.generate_successor(agent, action)
            score, _ = expectimax(succ, depth, 1)
            if score > max_score:
                max_score = score
                best_action = action
        return max_score, best_action

    else:  # Ghost (Expected)
        actions = state.get_legal_actions(state.ghost_pos)
        scores = []
        for action in actions:
            succ = state.generate_successor(agent, action)
            score, _ = expectimax(succ, depth-1, 0)
            scores.append(score)
        avg_score = sum(scores) / len(scores) if scores else 0
        return avg_score, None

def draw(state):
    SCREEN.fill(BLACK)
    for f in state.food:
        pygame.draw.circle(SCREEN, WHITE, (f[0]*CELL_SIZE + 20, f[1]*CELL_SIZE + 20), 5)
    pygame.draw.rect(SCREEN, YELLOW, (state.pacman_pos[0]*CELL_SIZE, state.pacman_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(SCREEN, RED, (state.ghost_pos[0]*CELL_SIZE, state.ghost_pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# Main Loop
def main():
    pacman_pos = (1, 1)
    ghost_pos = (10, 10)
    food = {(random.randint(0, COLS-1), random.randint(0, ROWS-1)) for _ in range(10)}
    score = 0

    state = GameState(pacman_pos, ghost_pos, food, score)
    running = True

    while running:
        CLOCK.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Pacman decision (Minimax or Expectimax)
        _, action = expectimax(state, 3, 0)
        if action:
            state = state.generate_successor(0, action)

        # Ghost decision (Random)
        ghost_actions = state.get_legal_actions(state.ghost_pos)
        if ghost_actions:
            ghost_action = random.choice(ghost_actions)
            state = state.generate_successor(1, ghost_action)

        draw(state)

        if state.is_win():
            print("Pacman Wins! Score:", state.score)
            running = False
        if state.is_lose():
            print("Ghost Caught Pacman! Score:", state.score)
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
