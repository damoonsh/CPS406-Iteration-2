from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import random

from utils import *
import consts

clock = pygame.time.Clock()

class Enemy:
    """ Manages the obstacles within the game """
    class _Qix:
        """ Implementing the logic for Qix Object. """
        def __init__(self):
            self.x, self.y = self._random_position()
            self.moves = ['down', 'up', 'left', 'right']

        def _random_position(self):
            """ Generates a random position for qix """
            x = random.randrange(consts.MARGIN, consts.MAP_WIDTH - consts.MARGIN)
            y = random.randrange(consts.MARGIN, consts.MAP_HEIGHT - consts.MARGIN)

            return x, y

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
            else:
                self.y -= consts.QIX_DIM

        def _move_up(self):
            if self.y > consts.MARGIN + consts.QIX_DIM:
                self.y -= consts.QIX_DIM * 2
            else:
                self.y += consts.QIX_DIM

        def _move_right(self):
            if self.x < consts.MAP_WIDTH - consts.MARGIN - consts.QIX_DIM:
                self.x += consts.QIX_DIM * 2
            else:
                self.x -= consts.QIX_DIM

        def _move_left(self):
            if self.x > consts.MARGIN + consts.QIX_DIM:
                self.x -= consts.QIX_DIM * 2
            else:
                self.x += consts.QIX_DIM

    class _Sparx:
        """ Implementing the logic for Sparx Object. """
        def __init__(self):
            self.dir = None  # up, down, left, right of the grid
            self.x, self.y, self.orientation = self._random_position()

        def get_coordinate(self):
            return self.x, self.y

        def get_orientation(self):
            return self.orientation

        def _random_position(self):
            """ Return random positions for sparx """
            fix_x = [consts.MARGIN, consts.MAP_WIDTH - consts.MARGIN]
            fix_y = [consts.MARGIN, consts.MAP_HEIGHT - consts.MARGIN]
            
            # 0: Vertical
            if random.choice([0, 1]) == 0:
                x = random.choice(fix_x)
                if x == consts.MARGIN: # to set initial direction
                    self.dir = 'left'
                else:
                    self.dir = 'right'
                y = random.randrange(consts.MARGIN // 5, (consts.MAP_HEIGHT - consts.MARGIN) // 5) * 5
                return x, y, 'vertical'
            else:
                x = random.randrange(consts.MARGIN // 5, (consts.MAP_WIDTH - consts.MARGIN) // 5) * 5
                y = random.choice(fix_y)
                if y == consts.MARGIN: # to set initial direction
                    self.dir = 'up'
                else:
                    self.dir = 'down'
                return x, y, 'horizontal'

        def next_move(self):
            if self.dir == 'up':
                if self.x + consts.MOVE_DIM < consts.MAP_WIDTH - consts.MARGIN:
                    self.x += consts.MOVE_DIM 
                else:
                    self.dir = 'right'
                    self.y += consts.MOVE_DIM

            elif self.dir == 'down':
                if self.x - consts.MOVE_DIM > consts.MARGIN:
                    self.x -= consts.MOVE_DIM 
                else:
                    self.dir = 'left'
                    self.y -= consts.MOVE_DIM

            elif self.dir == 'left':
                if self.y - consts.MOVE_DIM > consts.MARGIN:
                    self.y -= consts.MOVE_DIM
                else:
                    self.dir = 'up'
                    self.x += consts.MOVE_DIM

            else:  # if self.dir == 'right':
                if self.y + consts.MOVE_DIM < consts.MAP_HEIGHT - consts.MARGIN:
                    self.y += consts.MOVE_DIM
                else:
                    self.dir = 'down'
                    self.x -= consts.MOVE_DIM

    def __init__(self):
        self.quixes = []
        self.sparxes = []
        self.init = True
    
    def _add_sparx(self):
        self.sparxes.append(Enemy._Sparx())

    def _add_qix(self):
        self.sparxes.append(Enemy._Qix())
    
    def update(self):
        if self.init:
            self._add_qix()
            self._add_sparx()
            self.init = False
        
        self._fetch_next_moves()

    def _fetch_next_moves(self):
        for sparx in self.sparxes:
            sparx.next_move()

        for quix in self.quixes:
            quix.next_move()


class Map:
    """ Main map that renders everything within here """

    def __init__(self, height: int = consts.MAP_HEIGHT, width: int = consts.MAP_WIDTH):
        self.width = width
        self.height = height

        # Initialize the pygame module
        pygame.init()

        self.life = Life()

        # Set the properties of the Display
        self.gameDisplay = pygame.display.set_mode((self.height, self.width))
        self.gameDisplay.fill(consts.BG_COLOR)

        # Setting the caption
        pygame.display.set_caption('QIX')

        self.player = Player()

        self.enemy = Enemy()

    def render(self):
        """ Renders the graphics """

        self.gameDisplay.fill(consts.BG_COLOR)

        # Draw the borders
        self._draw_borders()

        # Draw the player and the claimed areas
        self._draw_player()
        self._draw_clamied_areas()

        self.enemy.update()
        self._render_enemy()
    
        # Write the life text
        # Note: This should be rendered at the end to overwrite anything else!
        self.gameDisplay.blit(self.life.get_text(), self.life.get_coordinate())

    def _render_enemy(self):
        """ Renders the graphics for enemy objects. """

        for sparx in self.enemy.sparxes:
            self._draw_sparx(sparx)

        for quix in self.enemy.quixes:
            self._draw_qix(quix)


    def _draw_sparx(self, sparx: Enemy._Sparx, color=consts.SPARX_COLOR):
        x,y = sparx.get_coordinate()
        pygame.draw.polygon(self.gameDisplay,
                            color,
                            [(x, y), (x + consts.SPARX_DIM, y + consts.SPARX_DIM),
                             (x, y + 2 * consts.SPARX_DIM), (x - consts.SPARX_DIM, y + consts.SPARX_DIM)])

    def _draw_qix(self, quix: Enemy._Qix, color=consts.QIX_COLOR):
        x, y = quix.get_coordinate()
        pygame.draw.polygon(self.gameDisplay,
                            color,
                            [(x, y), (x + consts.QIX_DIM, y + consts.QIX_DIM),
                             (x, y + 2 * consts.QIX_DIM), (x - consts.QIX_DIM, y + consts.QIX_DIM)])

    def _draw_clamied_areas(self):
        pass

    def _draw_player(self):
        """ Draws the player """
        pygame.draw.circle(self.gameDisplay,
                           consts.PLAYER_COLOR,
                           self.player.get_coordinate(),
                           consts.PLAYER_RADIUS)

    def _draw_borders(self, margin: int = consts.MARGIN, color: (int, int, int) = consts.BORDER_COLOR):
        """ Draws the border for the QIX game """
        # Upper Horizontal Line
        pygame.draw.line(self.gameDisplay, color,
                         (margin, margin), (self.width - margin, margin))

        # Lower Horizontal Line
        pygame.draw.line(self.gameDisplay, color, (margin, self.height -
                                                   margin), (self.width - margin, self.height - margin))
        # Left Vertical Line
        pygame.draw.line(self.gameDisplay, color,
                         (margin, margin), (margin, self.height - margin))
        # Right Vertical Line
        pygame.draw.line(self.gameDisplay, color, (self.width - margin,
                                                   margin), (self.width - margin, self.height - margin))


# Initialization
PAUSE = False
map = Map()
map.render()

while True:
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