import pygame
import MazeLayouts

# 31 * 15
SingleAgentMazeLayout = MazeLayouts.SingleAgentLayout

# 31 * 15
MultiAgentMazeLayout = MazeLayouts.MultiAgentLayout

# 37* 37
SingleAgentMazeBigLayout = MazeLayouts.SingleAgentMazeBigLayout

TILE_SIZE = 21
GRID_WIDTH,GRID_HEIGHT = len(MultiAgentMazeLayout[0]),len(MultiAgentMazeLayout)
WIDTH,HEIGHT = TILE_SIZE * GRID_WIDTH + 10,TILE_SIZE * GRID_HEIGHT + 10

pacman_right_path = [
	"assets/pacman-right/1.png",
	"assets/pacman-right/2.png",
	"assets/pacman-right/3.png"
]

pacman_left_path = [
	"assets/pacman-left/1.png",
	"assets/pacman-left/2.png",
	"assets/pacman-left/3.png"
]

pacman_up_path = [
	"assets/pacman-up/1.png",
	"assets/pacman-up/2.png",
	"assets/pacman-up/3.png"
]

pacman_down_path = [
	"assets/pacman-down/1.png",
	"assets/pacman-down/2.png",
	"assets/pacman-down/3.png"
]

blinky_ghost = "assets/ghosts/blinky.png"
blue_ghost = "assets/ghosts/blue_ghost.png"
clyde_ghost = "assets/ghosts/clyde.png"
inky_ghost = "assets/ghosts/inky.png"
pinky_ghost = "assets/ghosts/pinky.png"

start_menu_keys = {
	pygame.K_a: 'single_goal_menu',
	pygame.K_b: 'multigoal_menu',
}

single_goal_menu_keys = {
	pygame.K_a: 'dfs',
	pygame.K_b: 'bfs',
	pygame.K_c: 'ucs',
	pygame.K_d: 'a_star',
	pygame.K_e: 'greedy',
}

multigoal_menu_keys = {
	pygame.K_a: 'dfs',
	pygame.K_b: 'bfs',
}

single_agent_game_mode = [
	("a- Single Goal",pygame.K_a),
	("b- Multiple Goal",pygame.K_b)
]
game_mode = [
	("a- Single Agent",pygame.K_a),
	("b- Multi Agent",pygame.K_b)
]
single_goal_options = [
	("a- DFS ",pygame.K_a),
	("b- BFS ",pygame.K_b),
	("c- UCS ",pygame.K_c),
	("d- A* Search",pygame.K_d),
	("e- Greedy Search",pygame.K_e)
]
multigoal_options = [
	("a- DFS ",pygame.K_a),
	("b- BFS ",pygame.K_b),
]

pacman_directions = {
	'r': pacman_right_path,
	'l': pacman_left_path,
	'u': pacman_up_path,
	'd': pacman_down_path
}

from Search import *

search_algorithms = {
	'dfs': dfs,
	'bfs': bfs,
	'ucs': ucs,
	'a_star': a_star,
	'greedy': greedy
}

movement_direction = {
	(-1,0): 'r',
	(1,0): 'l',
	(0,-1): 'd',
	(0,1): 'u',
	(0,0) : 'r',
	(-GRID_WIDTH + 1,0): 'r',
	(GRID_WIDTH - 1,0): 'l',
}

BLUE = (25,25,166)
BLACK = (0,0,0)
TEAL = (0,128,128)
WHITE = (255,255,255)
GOAL_COLOR = (255,0,0)
GREEN = (0,255,0)
PATH_COLOR = (168,92,83)
VISITED_COLOR = (82,80,80)
DOT_COLOR = (255,255,255)
