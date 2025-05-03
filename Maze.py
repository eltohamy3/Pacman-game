from abc import abstractmethod

import Configuration
from Configuration import *

class Maze:
    def __init__(self):
        self.uneaten = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.goals = set()

    def eat_dot(self, x, y):
        if 0<=x<GRID_WIDTH and 0<=y<GRID_HEIGHT:
            self.uneaten[y][x] = False

    def is_not_eaten(self,x,y):
        if 0<=x<GRID_WIDTH and 0<=y<GRID_HEIGHT:
            return self.uneaten[y][x]
        return False

    def get_uneaten_dots(self):
        uneaten_dots = set()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.is_not_eaten(x,y):
                    uneaten_dots.add((x,y))
        return uneaten_dots

    def all_dots_eaten(self):
        return len(self.get_uneaten_dots()) == 0

    def is_gate(self,x,y):
        if 0<=x<GRID_WIDTH and 0<=y<GRID_HEIGHT:
            return self.layout[y][x] == 0 and (x == GRID_WIDTH - 1 or x == 0)
        return False

    def is_valid(self,x,y):
        if 0 <=x <GRID_WIDTH and 0 <=y < GRID_HEIGHT:
            return self.layout[y][x] == 0 or self.layout[y][x] == 2
        return False

    @abstractmethod
    def draw(self,screen,visited,path):
        pass

class MultiGoalMaze(Maze):
    def __init__(self):
        self.layout = SingleAgentMazeLayout
        super().__init__()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0:
                    self.goals.add((x,y))


        for x,y in self.goals:
            self.uneaten[y][x] = True

    def draw(self,screen,visited,path):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0 or self.layout[y][x] == 2:
                    rect = pygame.Rect(x * TILE_SIZE,y * TILE_SIZE,TILE_SIZE * 1.6,TILE_SIZE * 1.6)
                    pygame.draw.rect(screen,BLACK,rect)

        # Draw dots for goals that haven't been eaten yet
        for x,y in self.get_uneaten_dots():
            pygame.draw.circle(screen,DOT_COLOR,(x * TILE_SIZE + TILE_SIZE // 2,y * TILE_SIZE + TILE_SIZE // 2),4)


class SingleGoalMaze(Maze):
    def __init__(self):
        global GRID_HEIGHT,GRID_WIDTH
        self.layout = SingleAgentMazeLayout
        super().__init__()
        self.goals.add((1,GRID_HEIGHT - 2))
        for x,y in self.goals:
            self.uneaten[y][x] = True


    def draw(self,screen,visited,path):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0 or self.layout[y][x] == 2:
                    rect = pygame.Rect(x * TILE_SIZE,y * TILE_SIZE,TILE_SIZE * 1.6,TILE_SIZE * 1.6)
                    pygame.draw.rect(screen,BLACK,rect)

            # color all the nodes that have been visited
            for x,y in visited:
                pygame.draw.rect(screen,VISITED_COLOR,
                                 (x * TILE_SIZE + 7,y * TILE_SIZE + 7,TILE_SIZE,TILE_SIZE))
            # color the path to goal
            for x,y in path:
                pygame.draw.rect(screen,PATH_COLOR,(x * TILE_SIZE + 7,y * TILE_SIZE + 7,TILE_SIZE,TILE_SIZE))

        # Draw dots for goals that haven't been eaten yet
        for x,y in self.get_uneaten_dots():
            pygame.draw.circle(screen,DOT_COLOR,(x * TILE_SIZE + TILE_SIZE // 2,y * TILE_SIZE + TILE_SIZE // 2),4)

class MultiAgentMaze(Maze):
    def __init__(self):
        self.is_power_pellet = False
        self.layout = MultiAgentMazeLayout
        super().__init__()
        self.power_pellets = [(1,1),(1,GRID_HEIGHT - 2),(GRID_WIDTH - 2,1),(GRID_WIDTH - 2,GRID_HEIGHT - 2)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0:
                    self.goals.add((x, y))
        for x, y in self.goals:
            self.uneaten[y][x] = True
    def draw(self,screen,visited,path):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0 or self.layout[y][x] == 2:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 1.6, TILE_SIZE * 1.6)
                    pygame.draw.rect(screen, BLACK, rect)

        for x, y in self.get_uneaten_dots():
            pygame.draw.circle(screen, DOT_COLOR, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 4)
