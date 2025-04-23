import time
from pacman import *

pygame.init ( )
pygame.font.init ( )

class Maze :
    def __init__ ( self  , type) :
        self.layout = BIGMAZE
        self.uneaten = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.goals = set()
        self.type = type  # 0 single gole  , 1 multi gole, 2 multi agent

        if type ==1 :
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.layout[y][x] == 0:
                        self.goals.add((x, y))
        elif type==0:
            self.goals.add((1, GRID_HEIGHT - 2))
        elif type==2:
            self.goals.add((2,3))

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

    def is_gate(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.layout[y][x] == 0 and (x == GRID_WIDTH - 1 or x == 0), x
        return False

    def valid(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.layout[y][x] == 0
        return False

    def draw ( self , screen  , visited , path ) :
        for y in range ( GRID_HEIGHT ) :
            for x in range ( GRID_WIDTH ) :
                if self.layout [y] [x] == 0 or self.layout [y] [x] == 2 :
                    rect = pygame.Rect ( x * TILE_SIZE , y * TILE_SIZE , TILE_SIZE * 1.6 , TILE_SIZE * 1.6 )
                    pygame.draw.rect ( screen , BLACK , rect )

        if(self.type == 0):
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
        self.start_pos = (GRID_WIDTH - 2 , GRID_HEIGHT - 2)
        # self.start_pos = (24 , 7)
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
        self.maze.draw ( self.screen  , self.pacman.visited_nodes , self.pacman.original_path )
        # if not self.pacman.all_goals_reached:
        self.pacman.draw ( self.screen )

        goals_eaten = len(self.maze.goals) - len(self.maze.get_uneaten_dots())
        total_goals = len(self.maze.goals)
        progress_text = f"Goals: {goals_eaten}/{total_goals}"
        txt = self.font.render(progress_text, True, WHITE)
        self.screen.blit(txt, (10, 5))

        if self.pacman.all_goals_reached:
            self.end_time = self.end_time or time.time()
            elapsed = round(self.end_time - self.start_time, 2)

            # Draw a semi-transparent background
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))  # Black with transparency
            self.screen.blit(s, (0, 0))

            if self.maze.type ==0 :
                stats = [
                    f"{self.algorithm.upper()} - Goal Reached!",
                    f"Time: {elapsed}s",
                    f"Visited: {len(self.pacman.visited_nodes)}",
                    f"Path Length: {len(self.path_history)}",
                    "Press R to Restart or Q to Quit"
                ]
            elif self.maze.type ==1 :  
                stats = [
                    f"{self.algorithm.upper()} - Goal Reached!",
                    f"Time: {elapsed}s",
                    f"Path Length: {len(self.path_history)}",
                    "Press R to Restart or Q to Quit"
                ]
            else :  
                stats = [
                    f"{self.algorithm.upper()} - Goal Reached!",
                    f"Time: {elapsed}s",
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
                            self.maze= Maze(0)
                        else:
                            self.maze= Maze(1)
                        self.set_algorithm ( keys [event.key] )
                        selecting = False

    def reset ( self ) :
        self.start_menu ( )
        self.run()

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


