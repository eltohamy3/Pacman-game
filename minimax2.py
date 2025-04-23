import math
import random
import pygame
import time
import copy
from collections import deque

# Initialize pygame
pygame.init()
pygame.font.init()

# Constants
TILE_SIZE = 21
GRID_WIDTH, GRID_HEIGHT = 31, 15
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH + 10, TILE_SIZE * GRID_HEIGHT + 10
FPS = 10

# Colors
BLUE = (24, 24, 217)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DOT_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
WALL_COLOR = (0, 0, 139)

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
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Maze:
    def __init__(self, layout):
        self.grid = layout
        self.height = len(layout)
        self.width = len(layout[0])
        self.pellets = {(r,c) for r in range(self.height) for c in range(self.width) if layout[r][c]==0}

    def can_move(self, x, y):
        return 0<=x<self.height and 0<=y<self.width and self.grid[x][y]!=1

    def eat_dot(self, pos):
        self.pellets.discard(pos)

    def all_dots_eaten(self):
        return not self.pellets

    def get_uneaten_dots(self):
        return set(self.pellets)

    def draw(self, screen):
        for r in range(self.height):
            for c in range(self.width):
                rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.grid[r][c]==1:
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                else:
                    pygame.draw.rect(screen, BLACK, rect)
                if (r,c) in self.pellets:
                    pygame.draw.circle(screen, DOT_COLOR, rect.center, 4)

def get_successors(pos, maze):
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    return [(pos[0]+dx,pos[1]+dy) for dx,dy in moves if maze.can_move(pos[0]+dx,pos[1]+dy)]

def evaluation_function(p_pos, g_pos, maze):
    if p_pos==g_pos:
        return -999
    dots=maze.get_uneaten_dots()
    if not dots:
        return 999
    dist_dot = min(abs(p_pos[0]-d[0])+abs(p_pos[1]-d[1]) for d in dots)
    dist_ghost = abs(p_pos[0]-g_pos[0])+abs(p_pos[1]-g_pos[1])
    return -dist_dot + dist_ghost*0.5 - len(dots)

def clone_maze(m):
    new = Maze(m.grid)
    new.pellets = set(m.pellets)
    return new

class Pacman:
    def __init__(self, pos, maze):
        self.pos=pos
        self.maze=maze

    def move(self, ghost_pos):
        _,mv=self.max_value(self.pos, ghost_pos, depth=3)
        self.pos=mv
        self.maze.eat_dot(self.pos)

    def max_value(self, p_pos, g_pos, depth):
        if depth==0 or p_pos==g_pos or self.maze.all_dots_eaten():
            return evaluation_function(p_pos,g_pos,self.maze), p_pos
        v=-math.inf; best=p_pos
        for nxt in get_successors(p_pos,self.maze):
            m=clone_maze(self.maze)
            m.eat_dot(nxt)
            val,_ = Pacman(nxt,m).min_value(nxt,g_pos,depth-1)
            if val>v: v, best=val, nxt
        return v,best

    def min_value(self, p_pos, g_pos, depth):
        if depth==0 or p_pos==g_pos or self.maze.all_dots_eaten():
            return evaluation_function(p_pos,g_pos,self.maze), g_pos
        v=math.inf; best=g_pos
        for nxt in get_successors(g_pos,self.maze):
            val,_ = self.max_value(p_pos,nxt,depth-1)
            if val<v: v,best=val,nxt
        return v,best

class Ghost:
    def __init__(self,pos,maze):
        self.pos=pos
        self.maze=maze

    def move(self,pac_pos):
        _,mv=minimax(pac_pos, self.pos, self.maze, depth=3, is_max=False)
        self.pos=mv

    def draw(self,screen):
        rect=pygame.Rect(self.pos[1]*TILE_SIZE,self.pos[0]*TILE_SIZE,TILE_SIZE,TILE_SIZE)
        pygame.draw.circle(screen,GHOST_COLOR,rect.center,TILE_SIZE//2)

def minimax(p_pos, g_pos, maze, depth, is_max):
    if depth == 0 or p_pos == g_pos or maze.all_dots_eaten():
        return evaluation_function(p_pos, g_pos, maze), p_pos if is_max else g_pos

    if is_max:
        v = -math.inf
        best = p_pos
        for nxt in get_successors(p_pos, maze):
            m = clone_maze(maze)
            m.eat_dot(nxt)
            val, _ = minimax(nxt, g_pos, m, depth - 1, False)
            if val > v:
                v, best = val, nxt
        return v, best
    else:
        v = math.inf
        best = g_pos
        for nxt in get_successors(g_pos, maze):
            val, _ = minimax(p_pos, nxt, maze, depth - 1, True)
            if val < v:
                v, best = val, nxt
        return v, best

# Main game loop
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
maze=Maze(BIGSEARCH)
pacman=Pacman((10,1),maze)
ghost=Ghost((29,13),maze)
running=True

while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT: running=False

    pacman.move(ghost.pos)
    ghost.move(pacman.pos)

    screen.fill(BLUE)
    maze.draw(screen)
    pygame.draw.circle(screen,GREEN,(pacman.pos[1]*TILE_SIZE+TILE_SIZE//2,pacman.pos[0]*TILE_SIZE+TILE_SIZE//2),TILE_SIZE//2)
    ghost.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

    if pacman.pos==ghost.pos:
        print("Game Over")
        running=False
    if maze.all_dots_eaten():
        print("You Win!")
        running=False

pygame.quit()