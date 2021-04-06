"""
    This file contains the constants used
    throughout the program
"""
# Colors
BG_COLOR = (0, 0, 0)
PLAYER_COLOR = (0, 255, 0)
QIX_COLOR = (255, 0, 0)
BORDER_COLOR = (255, 255, 255)
FONT_COLOR = (90, 90, 90)
SPARX_COLOR = (100, 2, 245)
INCURSION_BAD_COLOR = (255, 155, 155)
INCURSION_GOOD_COLOR = (77, 166, 255)
CLAIMED_AREA_COLOR = (77, 166, 255)

# Constants for font
FONT_SIZE = 20

# Constants used in the Game
PLAYER_RADIUS = QIX_DIM = SPARX_DIM = 10
MARGIN = 20
MAP_DIM = 420
MOVE_DIM = PLAYER_RADIUS
MAP_WIDTH = MAP_DIM
MAP_HEIGHT = MAP_DIM
MAP_AREA = (MAP_HEIGHT - MARGIN) * (MAP_WIDTH - MARGIN)

# Constants related to life
INIT_LIFE = 10
INIT_COOR = (5, 2)
QIX_DAMAGE = 1
SPARX_DAMAAGE = 2

# Frames Per second
FPS = 16