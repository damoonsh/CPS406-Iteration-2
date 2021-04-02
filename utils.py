import pygame
import consts
import random

clock = pygame.time.Clock()

class Point:
    """
        Point Object storing the properties and attributes
        of a pixel within the pixelArray.
    """

    def __init__(self, x: int, y: int, move: str):
        self.x = x
        self.y = y
        self.passer = []
        self.move = move

    def add_passer(self, passer):
        self.passer.append(passer)


class Player:
    """
        Player Object that implements the logic of the
        player moving in the map.
    """

    def __init__(self):
        self.points = []
        self.x = (consts.MAP_WIDTH - consts.MARGIN) // 2
        self.y = 400
        self.claiming = False
        self.previous_direction = None
        self.life_force = 100

    def get_coordinate(self):
        return (self.x, self.y)

    def move(self, direction: str):
        """ Controls the movement of the player """
        if self.previous_direction != direction:
            self.previous_direction == direction

        if self.claiming:
            self.points.append(Point(self.x, self.y, direction))

        if direction == 'right':
            self._move_right()
        if direction == 'left':
            self._move_left()
        if direction == 'up':
            self._move_up()
        if direction == 'down':
            self._move_down()

    def _move_right(self):
        if self.x != consts.MAP_WIDTH - consts.MARGIN:
            self.x += consts.PLAYER_RADIUS

    def _move_left(self):
        if self.x != consts.MARGIN:
            self.x -= consts.PLAYER_RADIUS

    def _move_up(self):
        if self.y != consts.MARGIN:
            self.y -= consts.PLAYER_RADIUS

    def _move_down(self):
        if self.y != consts.MAP_HEIGHT - consts.MARGIN:
            self.y += consts.PLAYER_RADIUS


class Enemy:
    """
        Manages the obstacles within the game 
    """
    class _Qix:
        def __init__(self):
            self.x = random.randrange(consts.MARGIN*2, consts.MAP_WIDTH - consts.MARGIN) #random x position QIX starts at
            self.y = random.randrange(consts.MARGIN*2, consts.MAP_HEIGHT - consts.MARGIN) #random y position QIX starts at
            self.moves = ['down', 'up', 'left', 'right']

        def get_coordinate(self):
            return (self.x, self.y)

        def next_move(self):
            move = self.moves[random.randrange(0, 4)]
            if move == 'down': 
                self._move_down()
            if move == 'up': 
                self._move_up()
            if move == 'left': 
                self._move_left()
            if move == 'right': 
                self._move_right()

        def _move_down(self):
            if self.y < consts.MAP_HEIGHT - consts.MARGIN - consts.QIX_DIM:
                self.y += consts.QIX_DIM * 2
            else: self.y -= consts.QIX_DIM 

        def _move_up(self):
            if self.y > consts.MARGIN + consts.QIX_DIM:
                self.y -= consts.QIX_DIM * 2
            else: self.y += consts.QIX_DIM

        def _move_right(self):
            if self.x < consts.MAP_WIDTH - consts.MARGIN - consts.QIX_DIM:
                self.x += consts.QIX_DIM * 2
            else: self.x -= consts.QIX_DIM

        def _move_left(self):
            if self.x > consts.MARGIN + consts.QIX_DIM:
                self.x -= consts.QIX_DIM * 2
            else: self.x += consts.QIX_DIM

    class _Sparx:
        def __init__(self):
            self.x = (consts.MAP_WIDTH - consts.MARGIN) // 2
            self.y = consts.MARGIN - consts.SPARX_DIM
            self.dir = 'N' # North, East, South, West border of grid

        def next_move(self):

            if self.dir == 'N':
                if self.x + consts.SPARX_DIM > consts.MAP_WIDTH - consts.MARGIN:
                    self.dir = 'E'
                    self.y += consts.SPARX_DIM * 2
                else:
                    self.x += consts.SPARX_DIM * 2

            elif self.dir == 'S':
                if self.x - consts.SPARX_DIM < consts.MARGIN:
                    self.dir = 'W'
                    self.y -= consts.SPARX_DIM * 2
                else:
                    self.x -= consts.SPARX_DIM * 2

            elif self.dir == 'W':
                if self.y - consts.SPARX_DIM < consts.MARGIN:
                    self.dir = 'N'
                else:
                    self.y -= consts.SPARX_DIM * 2
            
            else: #if self.dir == 'E':
                if self.y + consts.SPARX_DIM > consts.MAP_HEIGHT - consts.MARGIN:
                    self.dir = 'S'
                else:
                    self.y += consts.SPARX_DIM * 2

    def __init__(self):
        self.quixes = []
        self.sparxes = []


class Map:
    """
        Main map that renders everything within here
    """

    def __init__(self, height: int = consts.MAP_HEIGHT, width: int = consts.MAP_WIDTH):
        self.width = width
        self.height = height

        # Initialize the pygame module
        pygame.init()

        # Set the properties of the Display
        self.gameDisplay = pygame.display.set_mode((self.height, self.width))
        self.gameDisplay.fill(consts.BG_COLOR)

        # Setting the caption
        pygame.display.set_caption('QIX')

        # Initializing the pixel property
        self.pixel = pygame.PixelArray(self.gameDisplay)

        self.enemy = Enemy()
        self.player = Player()
        self.qix = Enemy._Qix()
        self.sparx1 = Enemy._Sparx()
        
        self.sparx2 = Enemy._Sparx()
        self.sparx2.x = self.sparx2.x - 140
        self.sparx2.y = self.sparx2.y + consts.MAP_HEIGHT - 45 #setting y position of second sparx at bottom of map
        self.sparx2.dir = 'S'

        self.enemy.quixes.append(self.qix)
        self.enemy.sparxes.append(self.sparx1)
        self.enemy.sparxes.append(self.sparx2)

    def render(self):
        """ Renders the graphics """

        self.gameDisplay.fill(consts.BG_COLOR)

        # Draw the borders
        self._draw_borders()
        self._draw_player()
        self._draw_clamied_areas()
        self._draw_qix()
        self._draw_sparx(self.sparx1.x, self.sparx1.y)
        self._draw_sparx(self.sparx2.x, self.sparx2.y)

    def _draw_sparx(self, x, y):
        pygame.draw.polygon(self.gameDisplay,
                            consts.QIX_COLOR,
                            [(x, y), (x + consts.SPARX_DIM, y + consts.SPARX_DIM),
                             (x, y + 2 * consts.SPARX_DIM), (x - consts.SPARX_DIM, y + consts.SPARX_DIM)])

    def _draw_qix(self):
        pygame.draw.circle(self.gameDisplay,
                            consts.QIX_COLOR,
                            self.qix.get_coordinate(),
                            consts.QIX_DIM)

    def _draw_clamied_areas(self):
        pass

    def _draw_player(self):
        """ Draws the player """
        pygame.draw.circle(self.gameDisplay,
                           consts.PLAYER_COLOR,
                           self.player.get_coordinate(),
                           consts.PLAYER_RADIUS)

    def _draw_borders(self, thick: int = consts.BORDER_THICKNESS, margin: int = consts.MARGIN, color: (int, int) = consts.BORDER_COLOR):
        """ Draws the border for the QIX game """
        self.pixel[margin: self.width - margin, margin:margin +
                   thick] = color  # Upper Horizontal Line
        self.pixel[margin: self.width - margin, self.height -
                   margin:self.height - margin + thick] = color  # Lower Horizontal Line
        self.pixel[margin: margin+thick, margin:self.height -
                   margin] = color  # Left Vertical Line
        self.pixel[self.width - margin:self.width - margin + thick,
                   margin:self.height - margin] = color  # Right Vertical Line


# Initialization
PAUSE = False
map = Map()
map.render()

while True:
    map.qix.next_move()
    map.sparx1.next_move()
    map.sparx2.next_move()
    for event in pygame.event.get():

        # Quitting the game
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:

            # Starting to claim territory
            if event.key == pygame.K_SPACE:
                map.player.claiming = not map.player.claiming

            # Pausing
            if event.key == pygame.K_p:
                PAUSE = True

            # Moving manually
            if event.key == pygame.K_RIGHT:
                map.player.move(direction="right")

            if event.key == pygame.K_LEFT:
                map.player.move(direction="left")

            if event.key == pygame.K_UP:
                map.player.move(direction="up")

            if event.key == pygame.K_DOWN:
                map.player.move(direction="down")

    # If the game is not paused then render the graphics
    if not PAUSE:
        map.render()

    pygame.display.update()
    clock.tick(consts.FPS)
