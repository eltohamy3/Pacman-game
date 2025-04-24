import pygame
import mazeLayouts

# 31 * 15
BIGSEARCH = mazeLayouts.BIGSEARCH

# 37* 37
BIGMAZE = mazeLayouts.BIGMAZE

TILE_SIZE = 21
GRID_WIDTH, GRID_HEIGHT = len(BIGSEARCH[0]), len(BIGSEARCH)
WIDTH , HEIGHT = TILE_SIZE * GRID_WIDTH + 10 , TILE_SIZE * GRID_HEIGHT + 10

pacman_right_path = [
    "assets/pacman-right/1.png" ,
    "assets/pacman-right/2.png" ,
    "assets/pacman-right/3.png"
]

pacman_left_path = [
    "assets/pacman-left/1.png" ,
    "assets/pacman-left/2.png" ,
    "assets/pacman-left/3.png"
]

pacman_up_path = [
    "assets/pacman-up/1.png" ,
    "assets/pacman-up/2.png" ,
    "assets/pacman-up/3.png"
]

pacman_down_path = [
    "assets/pacman-down/1.png" ,
    "assets/pacman-down/2.png" ,
    "assets/pacman-down/3.png"
]

keys = {
    pygame.K_a : 'dfs' ,
    pygame.K_b : 'bfs' ,
    pygame.K_c : 'ucs' ,
    pygame.K_d : 'a_star' ,
    pygame.K_e : 'greedy' ,
    pygame.K_f: 'dfs',
    pygame.K_g: 'bfs',
    pygame.K_h: 'ucs',
    pygame.K_i: 'a_star',
    pygame.K_j: 'greedy',
}

options = [
    ("a- DFS (single goal)" , pygame.K_a) ,
    ("b- BFS (single goal)" , pygame.K_b) ,
    ("c- UCS (single goal)" , pygame.K_c) ,
    ("d- A* Search (single goal)" , pygame.K_d) ,
    ("e- Greedy Search (single goal)" , pygame.K_e) ,
    ("f- DFS (Multiple goals)", pygame.K_f),
    ("g- BFS (Multiple goals)", pygame.K_g),
    ("h- UCS (Multiple goals)", pygame.K_h),
    ("i- A* Search (Multiple goals)", pygame.K_i),
    ("j- Greedy Search (Multiple goals)", pygame.K_j),
]

pacman_directions = {
    'r' : pacman_right_path ,
    'l' : pacman_left_path ,
    'u' : pacman_up_path ,
    'd' : pacman_down_path
}

from search import *
search_algorithms = {
    'dfs': dfs,
    'bfs': bfs,
    'ucs': ucs,
    'a_star': a_star,
    'greedy': greedy
}

movement_direction = {
    (-1 , 0) : 'r' ,
    (1 , 0) : 'l' ,
    (0 , -1) : 'd' ,
    (0 , 1) : 'u',
    (-GRID_WIDTH + 1, 0) : 'r',
    (GRID_WIDTH - 1, 0) : 'l',
}

BLUE = (25 , 25 , 166)
BLACK = (0 , 0 , 0)
TEAL = (0 , 128 , 128)
WHITE = (255 , 255 , 255)
GOAL_COLOR = (255 , 0 , 0)
GREEN = (0 , 255 , 0)
PATH_COLOR = (168 , 92 , 83)
VISITED_COLOR = (82 , 80 , 80)
DOT_COLOR = (255, 255, 0)
