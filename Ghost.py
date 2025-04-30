from collections import deque

from Configuration import *


class Ghost:
	def __init__(self,x,y,maze,game):
		self.pos = (x,y)
		self.prevPos = (x,y)
		self.maze = maze
		self.game = game
		self.moves = [(-1,0),(1,0),(0,-1),(0,1)]
		self.path = []
		self.speed = 0.9  # Slower than Pacman
		self.move_counter = 0

	def find_path_to_pacman(self,pacman_pos):
		queue = deque([(self.pos,[])])
		visited = set()

		while queue:
			current,path = queue.popleft()
			if current == pacman_pos:
				self.path = path
				return

			for dx,dy in self.moves:
				nx,ny = current[0] + dx,current[1] + dy
				if self.maze.is_valid(nx,ny) and (nx,ny) not in visited:
					visited.add((nx,ny))
					queue.append(((nx,ny),path + [(nx,ny)]))
		self.path = []

	def move(self,pacman_pos):
		self.move_counter += 1
		if self.move_counter<1 / self.speed:
			return False

		self.move_counter = 0
		self.prevPos = self.pos
		self.find_path_to_pacman(pacman_pos)
		if self.path:
			self.pos = self.path[0]
			return True
		return False

	def draw(self,screen):
		x = self.pos[0] * TILE_SIZE
		y = self.pos[1] * TILE_SIZE
		ghost_img = pygame.image.load(blinky_ghost)
		ghost_img = pygame.transform.scale(ghost_img,(TILE_SIZE,TILE_SIZE))
		screen.blit(ghost_img,(x,y))

	def get_rect(self):
		return pygame.Rect(self.pos[0] * TILE_SIZE,self.pos[1] * TILE_SIZE,TILE_SIZE,TILE_SIZE)
