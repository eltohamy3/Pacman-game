# Constants
from mazeLayouts import mazeLayouts

TILE_SIZE = 21
# GRID_WIDTH, GRID_HEIGHT = 37, 37
GRID_WIDTH , GRID_HEIGHT = 31 , 15
WIDTH , HEIGHT = TILE_SIZE * GRID_WIDTH + 10 , TILE_SIZE * GRID_HEIGHT + 10
0
SEARCH_ALGO = 'dfs'

#configuration
pacman_right_path = [ "assets/pacman-right/1.png" ,
                      "assets/pacman-right/2.png" ,
                      "assets/pacman-right/3.png" ]

pacman_left_path = [ "assets/pacman-left/1.png" ,
                     "assets/pacman-left/2.png" ,
                     "assets/pacman-left/3.png" ]

pacman_up_path = [ "assets/pacman-up/1.png" ,
                   "assets/pacman-up/2.png" ,
                   "assets/pacman-up/3.png" ]

pacman_down_path = [ "assets/pacman-down/1.png" ,
                     "assets/pacman-down/2.png" ,
                     "assets/pacman-down/3.png" ]

# Colors
BLUE = (25 , 25 , 166)
BLACK = (0 , 0 , 0)
TEAL = (0 , 128 , 128)
WHITE = (255 , 255 , 255)
GOAL_COLOR = (255 , 0 , 0)
GREEN = (0 , 255 , 0)
PATH_COLOR = (168 , 92 , 83)
VISITED_COLOR = (82 , 80 , 80)

# 31 * 15
BIGSEARCH = mazeLayouts.BIGSEARCH

# 37* 37
BIGMAZE = mazeLayouts.BIGMAZE
