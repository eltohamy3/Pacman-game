import inspect
import time

from Maze import *
from pacman import *

pygame.init ()
pygame.font.init ()

class Game:
    def __init__ ( self ):
        self.screen = pygame.display.set_mode ((WIDTH,HEIGHT))
        pygame.display.set_caption ("Pacman Game")
        self.clock = pygame.time.Clock ()
        self.font = pygame.font.SysFont ('arial',20,bold = True)
        self.start_pos = (GRID_WIDTH - 2 , GRID_HEIGHT - 2)
        # self.start_pos = (15,GRID_HEIGHT - 2)
        self.running = True
        self.start_menu ()
        self.path_history = []

    def set_algorithm ( self,name ):
        self.algorithm = name
        self.pacman = Pacman (*self.start_pos,self.maze)
        self.start_time = time.time ()
        self.end_time = None

    def draw ( self ):
        self.screen.fill (BLUE)
        self.maze.draw (self.screen, self.pacman.visited_nodes, self.pacman.original_path)
        self.pacman.draw (self.screen)

        goals_eaten = len (self.maze.goals) - len (self.maze.get_uneaten_dots ())
        total_goals = len (self.maze.goals)
        progress_text = f"Goals: {goals_eaten}/{total_goals}"
        txt = self.font.render (progress_text,True,WHITE)
        self.screen.blit (txt,(10,5))

        if self.pacman.all_goals_reached:
            self.end_time = self.end_time or time.time ()
            elapsed = round (self.end_time - self.start_time,2)

            # Draw a semi-transparent background
            s = pygame.Surface ((WIDTH,HEIGHT),pygame.SRCALPHA)
            s.fill ((0,0,0,180))  # Black with transparency
            self.screen.blit (s,(0,0))

            if inspect.isabstract(SingleGoalMaze):
                stats = [
                    f"{self.algorithm.upper ()} - Goal Reached!",
                    f"Time: {elapsed}s",
                    f"Visited: {len (self.pacman.visited_nodes)}",
                    f"Path Length: {len (self.path_history)}",
                    "Press R to Restart or Q to Quit"
                ]
            elif inspect.isabstract(MultiGoalMaze):
                stats = [
                    f"{self.algorithm.upper ()} - Goal Reached!",
                    f"Time: {elapsed}s",
                    f"Path Length: {len (self.path_history)}",
                    "Press R to Restart or Q to Quit"
                ]
            else:
                stats = [
                    f"{self.algorithm.upper ()} - Goal Reached!",
                    f"Time: {elapsed}s",
                    "Press R to Restart or Q to Quit"
                ]
            for i,line in enumerate (stats):
                txt = self.font.render (line,True,GREEN)
                self.screen.blit (txt,(WIDTH // 2 - txt.get_width () // 2,100 + i * 30))

        pygame.display.flip ()

    def update ( self ):
        if not self.pacman.all_goals_reached:
            # If we have no current path, find the next path
            if not self.pacman.path:
                self.pacman.find_next_path (self.algorithm)

            # Move along the current path
            if self.pacman.move ():
                self.path_history.append (self.pacman.pos)
                pygame.time.wait (120)  # Delay for visualization

    def get_key ( self ):
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit ()
                exit ()
            elif event.type == pygame.KEYDOWN:
                return event.key
        return -1

    def display_screen(self, text, mode):
        self.screen.fill(BLACK)
        self.font = pygame.font.Font(None, 40)
        title = self.font.render(text, True, GREEN)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
        self.font = pygame.font.Font(None, 30)
        for i, (text, _) in enumerate(mode):
            option_text = self.font.render(text, True, WHITE)
            self.screen.blit(option_text, (20, 120 + i * 40))
        pygame.display.flip()

    def single_goal_start_menu ( self ):
        selecting = True
        self.maze = SingleGoalMaze()
        while selecting:
            self.display_screen("Single goal", single_goal_options)
            key = self.get_key()
            if key in single_goal_menu_keys:
                self.set_algorithm (single_goal_menu_keys [key])
                selecting = False

    def multigoal_start_menu ( self ):
        selecting = True
        self.maze = MultiGoalMaze()
        while selecting:
            self.display_screen("Multigoal goal", multigoal_options)
            key = self.get_key()
            if key in multigoal_menu_keys:
                self.set_algorithm (multigoal_menu_keys [key])
                selecting = False

    def start_menu ( self ):
        selecting = True
        while selecting:
            self.display_screen("Select Game Mode", game_mode)
            key = self.get_key()
            if key in start_menu_keys:
                if key == pygame.K_a:
                    self.single_goal_start_menu ()
                else:
                    self.multigoal_start_menu ()
                selecting = False

    def reset ( self ):
        self.start_menu ()
        self.run ()

    def run ( self ):
        while self.running:
            self.clock.tick (30)
            for event in pygame.event.get ():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.pacman.all_goals_reached:
                        if event.key == pygame.K_r:
                            self.reset ()
                        elif event.key == pygame.K_q:
                            self.running = False
            self.update ()
            self.draw ()
        pygame.quit ()


if __name__ == "__main__":
    game = Game ()
    game.run ()
