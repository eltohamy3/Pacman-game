import pygame
from configuration import TILE_SIZE,pacman_right_path,pacman_left_path,pacman_up_path,pacman_down_path

class Pacman :
    def __init__ ( self , x , y ) :
        self.pos = [x , y]
        self.dir = "r"
        self.prevPos = [x , y]
        self.path = []
        self.reached_goal = False
        self.frame_idx = 0

    def move_along_path ( self ) :
        if self.path :
            self.prevPos = self.pos
            self.pos = self.path.pop ( 0 )
            pygame.time.wait (100)
            if not self.path :
                self.reached_goal = True

    def get_direction ( self , screen ) :
        (pos_x , pos_y) = (self.prevPos [0] - self.pos [0] , self.prevPos [1] - self.pos [1])
        self.dir = { (-1 , 0) : 'r' , (1 , 0) : 'l' , (0 , -1) : 'd' , (0 , 1) : 'u' }.get ( (pos_x , pos_y) )

    def update_frame ( self , screen ) :
        x = self.pos [0] * TILE_SIZE
        y = self.pos [1] * TILE_SIZE
        pacman_dir = { 'r' : pacman_right_path , 'l' : pacman_left_path , 'u' : pacman_up_path ,
                       'd' : pacman_down_path }.get ( self.dir )
        self.frame_idx = self.frame_idx % len ( pacman_dir )
        pacman_img = pygame.image.load ( pacman_dir [self.frame_idx] )
        pacman_img = pygame.transform.scale ( pacman_img , (TILE_SIZE , TILE_SIZE) )
        screen.blit ( pacman_img , (x , y) )
        self.frame_idx += 1

    def draw ( self , screen ) :
        self.get_direction ( screen )
        self.update_frame ( screen )
