import time
from typing import Deque , Tuple , Optional

from configuration import *
from search import *
from pacman import *

pygame.init ( )
pygame.font.init ( )

class Maze :
    def __init__ ( self ) :
        self.layout = BIGSEARCH
    def rows_len(self):
        return  len (  self.layout )
    def columns_len ( self ) :
        return len (  self.layout [0] ) if len (self.layout ) else 0

    def can_move ( self , x , y ) :
        return GRID_WIDTH > x >= 0 == self.layout [y] [x] and 0 <= y < GRID_HEIGHT
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

        if goal :
            gx , gy = goal
            pygame.draw.circle ( screen , GOAL_COLOR ,
                                 (gx * TILE_SIZE + TILE_SIZE // 2 , gy * TILE_SIZE + TILE_SIZE // 2) ,
                                 6 )


class Game :
    def __init__ ( self ) :
        self.screen = pygame.display.set_mode ( (WIDTH , HEIGHT) )
        pygame.display.set_caption ( "Pacman Game" )
        self.clock = pygame.time.Clock ( )
        self.font = pygame.font.SysFont ( 'arial' , 20 , bold = True )
        self.maze = Maze ( )
        self.start_pos = (1 , 1)
        self.goal_pos = (29 , 13)
        self.running = True
        self.start_menu ( )
    def set_algorithm ( self , name ) :
        self.algorithm = name
        self.pacman = Pacman ( *self.start_pos )
        self.start_time = time.time ( )
        self.end_time = None
        search_fn = { 'dfs' : dfs , 'bfs' : bfs , 'ucs' : ucs , 'astar' : a_star , 'greedy' : greedy }.get ( name )
        if search_fn :
            self.pacman.path , self.visited_nodes = search_fn(self.maze,self.start_pos,self.goal_pos)
            self.original_path = list ( self.pacman.path )
        else :
            self.visited_nodes = set ( )
            self.original_path = []

    def draw ( self ) :
        self.screen.fill ( BLUE )
        self.maze.draw ( self.screen , self.goal_pos , self.visited_nodes , self.original_path )
        self.pacman.draw ( self.screen )

        if self.pacman.reached_goal :
            self.end_time = self.end_time or time.time ( )
            elapsed = round ( self.end_time - self.start_time , 2 )
            stats = [
                f"{self.algorithm.upper ( )} - Goal Reached!" ,
                f"Time: {elapsed}s" ,
                f"Visited: {len ( self.visited_nodes )}" ,
                f"Path Length: {len ( self.original_path )}" ,
                "Press R to Restart or Q to Quit"
            ]
            for i , line in enumerate ( stats ) :
                txt = self.font.render ( line , True , GREEN )
                self.screen.blit ( txt , (10 , HEIGHT - (len ( stats ) - i) * 24) )

        pygame.display.flip ( )

    def update ( self ) :
        if not self.pacman.reached_goal :
            self.pacman.move_along_path ( )

    def end_menu ( self ) :
        self.screen.fill ( BLACK )
        title = self.font.render ( "Select Search Algorithm" , True , GREEN )
        self.screen.blit ( title , (WIDTH // 2 - title.get_width ( ) // 2 , 50) )

        options = [
            ("1 - DFS" , pygame.K_1) ,
            ("2 - BFS" , pygame.K_2) ,
            ("3 - UCS" , pygame.K_3) ,
            ("4 - A*" , pygame.K_4) ,
            ("5 - Greedy Best-First" , pygame.K_5) ,
        ]

        for i , (text , _) in enumerate ( options ) :
            option_text = self.font.render ( text , True , WHITE )
            self.screen.blit ( option_text , (WIDTH // 2 - option_text.get_width ( ) // 2 , 120 + i * 40) )

        pygame.display.flip ( )

        for event in pygame.event.get ( ) :
            if event.type == pygame.QUIT :
                pygame.quit ( )
                exit ( )
            elif event.type == pygame.KEYDOWN :
                keys = {
                    pygame.K_1 : 'dfs' ,
                    pygame.K_2 : 'bfs' ,
                    pygame.K_3 : 'ucs' ,
                    pygame.K_4 : 'astar' ,
                    pygame.K_5 : 'greedy' ,
                }
                if event.key in keys :
                    self.set_algorithm ( keys [event.key] )
                    selecting = False

    def start_menu ( self ) :
        selecting = True
        while selecting :
            self.screen.fill ( BLACK )
            title = self.font.render ( "Select Search Algorithm" , True , GREEN )
            self.screen.blit ( title , (WIDTH // 2 - title.get_width ( ) // 2 , 50) )

            options = [
                ("1 - DFS" , pygame.K_1) ,
                ("2 - BFS" , pygame.K_2) ,
                ("3 - UCS" , pygame.K_3) ,
                ("4 - A*" , pygame.K_4) ,
                ("5 - Greedy Best-First" , pygame.K_5) ,
            ]

            for i , (text , _) in enumerate ( options ) :
                option_text = self.font.render ( text , True , WHITE )
                self.screen.blit ( option_text , (WIDTH // 2 - option_text.get_width ( ) // 2 , 120 + i * 40) )

            pygame.display.flip ( )

            for event in pygame.event.get ( ) :
                if event.type == pygame.QUIT :
                    pygame.quit ( )
                    exit ( )
                elif event.type == pygame.KEYDOWN :
                    keys = {
                        pygame.K_1 : 'dfs' ,
                        pygame.K_2 : 'bfs' ,
                        pygame.K_3 : 'ucs' ,
                        pygame.K_4 : 'astar' ,
                        pygame.K_5 : 'greedy' ,
                    }
                    if event.key in keys :
                        self.set_algorithm ( keys [event.key] )
                        selecting = False

    def reset ( self ) :
        # Show the menu again
        self.start_menu ( )

        # Recreate Pacman and rerun the selected search
        self.pacman = Pacman ( *self.start_pos )
        self.start_time = time.time ( )
        self.end_time = None
        search_fn = { 'dfs' : dfs , 'bfs' : bfs , 'ucs' : ucs , 'astar' : a_star , 'greedy' : greedy }.get (
            self.algorithm )
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
                    if self.pacman.reached_goal :
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

