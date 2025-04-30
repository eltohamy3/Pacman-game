import math
import time
from collections import deque

from Configuration import *


class Pacman:
	def __init__(self,x,y,maze):
		self.pos = (x,y)
		self.dir = "r"
		self.prevPos = (x,y)
		self.path = []
		self.original_path = []
		self.frame_idx = 0
		self.maze = maze
		self.all_goals_reached = False
		self.visited_nodes = set()
		self.maze.eat_dot(x,y)

	def find_next_path(self,algorithm):
		self.path = []
		uneaten_dots = self.maze.get_uneaten_dots()

		if not uneaten_dots:
			self.all_goals_reached = True
			return

		search_fn = search_algorithms.get(algorithm)
		if search_fn:
			self.path,visited = search_fn(self.maze,self.pos)
			self.original_path = list(self.path)
			self.visited_nodes.update(visited)

	# override
	def move(self):
		if self.path:
			self.prevPos = self.pos
			self.pos = self.path.pop(0)

			# Eat the dot
			self.maze.eat_dot(self.pos[0],self.pos[1])

			# Check if we've reached all goals
			if self.maze.all_dots_eaten():
				self.all_goals_reached = True
			return True
		return False

	def get_direction(self,screen):
		(pos_x,pos_y) = (self.prevPos[0] - self.pos[0],self.prevPos[1] - self.pos[1])
		self.dir = movement_direction.get((pos_x,pos_y))

	def update_frame(self,screen):
		x = self.pos[0] * TILE_SIZE
		y = self.pos[1] * TILE_SIZE

		pacman_dir = pacman_directions.get(self.dir)
		self.frame_idx = self.frame_idx % len(pacman_dir)

		pacman_img = pygame.image.load(pacman_dir[self.frame_idx])
		pacman_img = pygame.transform.scale(pacman_img,(TILE_SIZE,TILE_SIZE))
		screen.blit(pacman_img,(x,y))

		if not self.all_goals_reached:
			self.frame_idx += 1

	def draw(self,screen):
		self.get_direction(screen)
		self.update_frame(screen)


class MultiAgentPacman(Pacman):
	def __init__(self,x,y,maze):
		self.pos = (x,y)
		self.prevPos = (0,0)
		self.maze = maze
		self.original_path = []
		self.all_goals_reached = False
		self.dir = "r"
		self.score = 0
		self.alive = True
		self.moves = [(-1,0),(1,0),(0,-1),(0,1)]
		self.next_move = None
		self.speed = 1.2  # Faster than ghost
		self.move_counter = 0
		self.visited_nodes = set()
		self.last_dot_time = time.time()
		self.dot_check_interval = 2  # Check for nearest dot every 2 seconds
		self.frame_idx = 0

		if self.maze.is_not_eaten(x,y):
			self.maze.eat_dot(x,y)
			self.score += 10

	def find_nearest_dot(self):
		uneaten_dots = self.maze.get_uneaten_dots()
		if not uneaten_dots:
			return None

		# Find the nearest dot using BFS
		queue = deque([(self.pos,[])])
		visited = set()

		while queue:
			current,path = queue.popleft()
			if current in uneaten_dots:
				return path[0] if path else current

			for dx,dy in self.moves:
				nx,ny = current[0] + dx,current[1] + dy
				if self.maze.is_valid(nx,ny) and (nx,ny) not in visited:
					visited.add((nx,ny))
					queue.append(((nx,ny),path + [(nx,ny)]))
		return None

	def evaluate_state(self,pacman_pos,ghost_pos):
		"""Evaluation function for leaf nodes"""
		score = 0

		# Reward for eating dots
		if self.maze.is_not_eaten(pacman_pos[0],pacman_pos[1]):
			score += 100

		# Distance to nearest dot
		nearest_dot = self.find_nearest_dot()
		if nearest_dot:
			dot_dist = abs(pacman_pos[0] - nearest_dot[0]) + abs(pacman_pos[1] - nearest_dot[1])
			score -= dot_dist * 2

		# Ghost proximity
		ghost_dist = abs(pacman_pos[0] - ghost_pos[0]) + abs(pacman_pos[1] - ghost_pos[1])
		if ghost_dist<4:
			score -= (100 - ghost_dist * 20)
			if ghost_dist<2:
				score -= 200  # Very big penalty if ghost is very close

		return score

	def minimax(self,pacman_pos,ghost_pos,depth,maximizing_player,alpha=-math.inf,beta=math.inf):
		"""
		Minimax algorithm with alpha-beta pruning
		- maximizing_player: True for Pacman's turn, False for ghost's turn
		- depth: current depth in the tree
		"""
		# Base case: leaf node or terminal state
		if depth == 0 or self.is_terminal_state(pacman_pos,ghost_pos):
			return self.evaluate_state(pacman_pos,ghost_pos),pacman_pos

		if maximizing_player:  # Pacman's turn
			max_eval = -math.inf
			best_move = pacman_pos

			for dx,dy in self.moves:
				nx,ny = pacman_pos[0] + dx,pacman_pos[1] + dy
				isGate = self.maze.is_gate(*pacman_pos)
				if not self.maze.is_valid(nx,ny) and isGate:
					nx = 0 if pacman_pos[0] != 0 else GRID_WIDTH - 1
				if self.maze.is_valid(nx,ny) and (nx,ny) != ghost_pos:
					eval,_ = self.minimax((nx,ny),ghost_pos,depth - 1,False,alpha,beta)

					if eval>max_eval:
						max_eval = eval
						best_move = (nx,ny)

					alpha = max(alpha,eval)
					if beta<=alpha:
						break  # Beta cutoff

			return max_eval,best_move
		else:  # Ghost's turn (minimizing player)
			min_eval = math.inf
			best_move = ghost_pos

			for dx,dy in self.moves:
				nx,ny = ghost_pos[0] + dx,ghost_pos[1] + dy
				isGate = self.maze.is_gate(*ghost_pos)
				if not self.maze.is_valid(nx,ny) and isGate:
					nx = 0 if ghost_pos[0] != 0 else GRID_WIDTH - 1
				if self.maze.is_valid(nx,ny):
					eval,_ = self.minimax(pacman_pos,(nx,ny),depth - 1,True,alpha,beta)

					if eval<min_eval:
						min_eval = eval
						best_move = (nx,ny)

					beta = min(beta,eval)
					if beta<=alpha:
						break  # Alpha cutoff

			return min_eval,best_move

	def is_terminal_state(self,pacman_pos,ghost_pos):
		"""Check if the state is terminal (game over)"""
		# Check if pacman caught by ghost
		if pacman_pos == ghost_pos:
			return True

		# Check if all dots eaten
		if len(self.maze.get_uneaten_dots()) == 0:
			return True

		return False

	def minimax_decision(self,ghost_pos,depth=2):
		"""Make decision using minimax with specified depth"""
		_,best_move = self.minimax(self.pos,ghost_pos,depth,True)
		return best_move

	def update(self,ghost_pos):
		# Periodically check for nearest dot to prevent getting stuck
		if time.time() - self.last_dot_time>self.dot_check_interval:
			nearest_dot = self.find_nearest_dot()
			if nearest_dot:
				self.next_move = nearest_dot
			self.last_dot_time = time.time()
		else:
			# Use minimax with depth 2
			self.next_move = self.minimax_decision(ghost_pos,depth = 2)

	def move(self):
		self.move_counter += 1
		if self.move_counter<1 / self.speed:
			return False

		self.move_counter = 0
		if self.next_move and self.alive:
			self.prevPos = self.pos
			self.pos = self.next_move

			if self.maze.is_not_eaten(self.pos[0],self.pos[1]):
				self.maze.eat_dot(self.pos[0],self.pos[1])
				self.score += 10

			if self.maze.all_dots_eaten():
				self.all_goals_reached = True

			return True
		return False

	def get_rect(self):
		return pygame.Rect(self.pos[0] * TILE_SIZE,self.pos[1] * TILE_SIZE,TILE_SIZE,TILE_SIZE)
