import consts
import pygame

class Point:
    """ Storing Point information """

    def __init__(self, x: int, y: int, move: str):
        self.x = x
        self.y = y
        self.move = move


class Life:
    """ Renders lifetime of the player """

    def __init__(self, initial_life: int =consts.INIT_LIFE):
        pygame.font.init()
        self.life = initial_life
        self.font = pygame.font.SysFont('Comic Sans MS', consts.FONT_SIZE)

    def update(self, collision_type: str):
        """ 
            Updates the lives left after a collision 
            Note: Qix and Sparx have different damage levels!
        """
        if collision_type == 'Qix':
            self.life -= consts.QIX_DAMAGE
        else:
            self.life -= consts.SPARX_DAMAAGE

        return self.life <= 0

    def get_text(self):
        return self.font.render(f'Life: {self.life}', True, consts.FONT_COLOR)

    def get_coordinate(self):
        return consts.INIT_COOR


class Player:
    """
        Player Object that implements the logic of the
        player moving in the map.
    """

    def __init__(self):
        self.points = []
        self.x = (consts.MAP_WIDTH - consts.MARGIN) // 2
        self.y = consts.MAP_HEIGHT - consts.MARGIN
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
            self.x += consts.MOVE_DIM

    def _move_left(self):
        if self.x != consts.MARGIN:
            self.x -= consts.MOVE_DIM

    def _move_up(self):
        if self.y != consts.MARGIN:
            self.y -= consts.MOVE_DIM

    def _move_down(self):
        if self.y != consts.MAP_HEIGHT - consts.MARGIN:
            self.y += consts.MOVE_DIM