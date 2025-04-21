import time
from pacman import *

pygame.init ( )
pygame.font.init ( )

class Maze :
    def __init__ ( self ) :
        self.layout = BIGSEARCH
        self.uneaten = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.goals = set()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.layout[y][x] == 0:
                    self.goals.add((x, y))

    def initialize_goals(self, goal = None):
        # single goal
        if goal is not None :
            self.goals = goal

        # 2D array to track uneaten dots (True = uneaten, False = eaten)
        for x, y in self.goals:
            self.uneaten[y][x] = True


    def eat_dot(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.uneaten[y][x] = False

    def is_not_eaten(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.uneaten[y][x]
        return False

    def get_uneaten_dots(self):
        uneaten_dots = set()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.is_not_eaten(x, y):
                    uneaten_dots.add((x, y))
        return uneaten_dots

    def all_dots_eaten(self):
        return len(self.get_uneaten_dots()) == 0

    def rows_len(self):
        return  len (  self.layout )

    def columns_len ( self ) :
        return len (  self.layout [0] ) if len (self.layout ) else 0

    def valid ( self , x , y ) :
        return GRID_WIDTH > x >= 0 == self.layout [y][x] and 0 <= y < GRID_HEIGHT

    def draw ( self , screen , goal , visited , path ) :
        for y in range ( GRID_HEIGHT ) :
            for x in range ( GRID_WIDTH ) :
                if self.layout [y] [x] == 0 or self.layout [y] [x] == 2 :
                    rect = pygame.Rect ( x * TILE_SIZE , y * TILE_SIZE , TILE_SIZE * 1.6 , TILE_SIZE * 1.6 )
                    pygame.draw.rect ( screen , BLACK , rect )

        # color all the nodes that have been visited
        for x , y in visited :
            pygame.draw.rect ( screen , VISITED_COLOR ,
                               (x * TILE_SIZE + 7 , y * TILE_SIZE + 7 , TILE_SIZE , TILE_SIZE) )

        # color the path to goal
        for x , y in path :
            pygame.draw.rect ( screen , PATH_COLOR , (x * TILE_SIZE + 7 , y * TILE_SIZE + 7 , TILE_SIZE , TILE_SIZE) )

        # Draw dots for goals that haven't been eaten yet
        for x, y in self.get_uneaten_dots():
            pygame.draw.circle(screen, DOT_COLOR, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 4)

class Game :
    def __init__ ( self ) :
        self.screen = pygame.display.set_mode ( (WIDTH , HEIGHT) )
        pygame.display.set_caption ( "Pacman Game" )
        self.clock = pygame.time.Clock ( )
        self.font = pygame.font.SysFont ( 'arial' , 20 , bold = True )
        self.maze = Maze ( )
        self.start_pos = (GRID_WIDTH - 2 , GRID_HEIGHT - 2)
        self.goal_pos = {(1, GRID_HEIGHT - 2)}
        self.running = True
        self.start_menu ( )
        self.path_history = []

    def set_algorithm ( self , name ) :
        self.algorithm = name
        self.pacman = Pacman ( *self.start_pos, self.maze )
        self.start_time = time.time ( )
        self.end_time = None

    def draw ( self ) :
        self.screen.fill ( BLUE )
        self.maze.draw ( self.screen , self.goal_pos , self.pacman.visited_nodes , self.pacman.original_path )
        # if not self.pacman.all_goals_reached:
        self.pacman.draw ( self.screen )

        if self.pacman.all_goals_reached:
            self.end_time = self.end_time or time.time()
            elapsed = round(self.end_time - self.start_time, 2)

            # Draw a semi-transparent background
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))  # Black with transparency
            self.screen.blit(s, (0, 0))

            stats = [
                f"{self.algorithm.upper()} - Goal Reached!",
                f"Time: {elapsed}s",
                f"Visited: {len(self.pacman.visited_nodes)}",
                f"Path Length: {len(self.path_history)}",
                "Press R to Restart or Q to Quit"
            ]
            for i, line in enumerate(stats):
                txt = self.font.render(line, True, GREEN)
                self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 100 + i * 30))

        pygame.display.flip ( )

    def update(self):
        if not self.pacman.all_goals_reached:
            # If we have no current path, find the next path
            if not self.pacman.path:
                self.pacman.find_next_path(self.algorithm)

            # Move along the current path
            if self.pacman.move():
                self.path_history.append(self.pacman.pos)
                pygame.time.wait(120)  # Delay for visualization

    def start_menu ( self ) :
        selecting = True
        while selecting :
            self.screen.fill ( BLACK )
            self.font = pygame.font.Font(None, 40)
            title = self.font.render ( "Select Search Algorithm" , True , GREEN )
            self.screen.blit ( title , (WIDTH // 2 - title.get_width ( ) // 2 , 40) )
            self.font = pygame.font.Font(None, 24)

            for i , (text , _) in enumerate ( options ) :
                option_text = self.font.render ( text , True , WHITE )
                if(i < 5):
                    self.screen.blit (option_text , (20 , 120 + i * 40) )
                else:
                    self.screen.blit(option_text, (WIDTH // 2 + 20, 120 + (i - 5) * 40))

            pygame.display.flip ( )

            for event in pygame.event.get ( ) :
                if event.type == pygame.QUIT :
                    pygame.quit ( )
                    exit ( )
                elif event.type == pygame.KEYDOWN :
                    if event.key in keys :
                        if event.key < pygame.K_f:
                            self.maze.initialize_goals(self.goal_pos)
                        else:
                            self.maze.initialize_goals()
                        self.set_algorithm ( keys [event.key] )
                        selecting = False

    def reset ( self ) :
        # Show the menu again
        self.start_menu ( )

        # Recreate Pacman and rerun the selected search
        self.pacman = Pacman ( *self.start_pos, self.maze )
        self.start_time = time.time ( )
        self.end_time = None
        search_fn = search_algorithms.get (self.algorithm )
        if search_fn :
            self.pacman.path , self.visited_nodes = search_fn ( self.maze , self.start_pos , self.goal_pos )
            self.original_path = list ( self.pacman.path )
        else :
            self.visited_nodes = set ( )
            self.original_path = []

    def run ( self ) :
        while self.running :
            self.clock.tick ( 30 )
            for event in pygame.event.get ( ) :
                if event.type == pygame.QUIT :
                    self.running = False
                elif event.type == pygame.KEYDOWN :
                    if self.pacman.all_goals_reached :
                        if event.key == pygame.K_r :
                            self.reset ( )
                        elif event.key == pygame.K_q :
                            self.running = False
            self.update ( )
            self.draw ( )
        pygame.quit ( )

if __name__ == "__main__" :
    game = Game ( )
    game.run ( )