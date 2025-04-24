from configuration import *

class Pacman :
    def __init__ ( self , x , y, maze ) :
        self.pos = (x , y)
        self.dir = "r"
        self.prevPos = (x - 1 , y)
        self.path = []
        self.original_path = []
        self.frame_idx = 0
        self.maze = maze
        self.all_goals_reached = False
        self.visited_nodes = set()

        # Eat the starting position dot
        self.maze.eat_dot(x, y)
    def manhattanHeuristic (self, a , b ) :
        return abs(a [0] - b [0]) + abs(a [1] - b [1])

    def get_nearest_goal(self):
        self.path, visited = bfs(self.maze, self.pos)

        # closest_goal = None
        # min_distance = float('inf')
        #
        # for goal in goals:
        #     distance = self.manhattanHeuristic(start, goal)
        #     if distance < min_distance:
        #         closest_goal = goal
        #         min_distance = distance
        # return closest_goal

    def find_next_path(self, algorithm):
        self.path = []
        uneaten_dots = self.maze.get_uneaten_dots()

        if not uneaten_dots:
            self.all_goals_reached = True
            return
            
        # nearest_goal = self.get_nearest_goal(self.pos, uneaten_dots)
        # Find the next goal based on the algorithm
        if self.maze.type == 1:
            self.get_nearest_goal()
        else:
            search_fn = search_algorithms.get(algorithm)
            if search_fn :
                self.path, visited = search_fn(self.maze, self.pos)
                self.original_path = list (self.path)
                # Update visited nodes
                self.visited_nodes.update(visited)



    def move(self):
        if self.path:
            self.prevPos = self.pos
            self.pos = self.path.pop(0)

            # Eat the dot
            self.maze.eat_dot(self.pos[0], self.pos[1])

            # Check if we've reached all goals
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

    def draw ( self , screen ) :
        self.get_direction ( screen )
        self.update_frame ( screen )
