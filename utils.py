import consts
import pygame
import random


class Point:
    """ Storing Point information """

    def __init__(self, x: int, y: int, prev):
        self.x = x
        self.y = y
        self.prev = prev

    def get_coordinate(self):
        return (self.x, self.y)


class Text:
    """ Lives and claimed area text """

    def __init__(self, initial_life: int = consts.INIT_LIFE):
        pygame.font.init()
        self.life = initial_life
        self.font = pygame.font.SysFont('Comic Sans MS', consts.FONT_SIZE)

        self.claimed_percentage = 0

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

    def add_percentage(self, addittion_value):
        self.claimed_percentage += addittion_value

    def get_text(self):
        space = " " * (consts.MARGIN // 2)
        return self.font.render(f'{space}Life: {self.life}{space}Claimed Percentage: {self.claimed_percentage}%', True,
                                consts.FONT_COLOR)

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
        self.incursion_starting_point = None
        self.incursion_conditions_met = False
        self.previous_move = None
        self.life_force = 10
        self.claimed_area = 0
        # Claimed areas will be rendered via this list
        self.claimed_points = []
        self.current_incursion = []


    def get_coordinate(self):
        return (self.x, self.y)

    def add_incursion_point(self):
        x, y = self.get_coordinate()
        self.current_incursion.append([x, y])

    def get_total_claim_percentage(self):
        percentage_covered = round((self.claimed_area / consts.MAP_AREA) * 100.0)
        return percentage_covered

    def print_claimed_percentage(self):
        percentage = self.get_total_claim_percentage()
        print('Player has claimed: ' + str(percentage) + '%')

    def get_incursion_dimensions(self, a_list=None):
        if not a_list:
            width, height = find_displacement_in_list(self.current_incursion)
            width = abs(width)
            height = abs(height)
            return width, height
        else:
            width, height = find_displacement_in_list(a_list)
            width = abs(width)
            height = abs(height)
            return width, height

    def update_total_claimed_area(self):
        width, height = self.get_incursion_dimensions()
        self.claimed_area += width * height
        self.print_claimed_percentage()

    def update_total_claimed_area_qix_inside(self, boundary_list):
        width, height = find_displacement_in_list(boundary_list)
        self.claimed_area = 0
        self.claimed_area = consts.MAP_AREA - (width * height)
        self.print_claimed_percentage()

    def finish_incursion(self):
        self.update_total_claimed_area()
        self.claimed_points.append(self.current_incursion)
        self.incursion_starting_point = None
        self.current_incursion = []
        self.claiming = False
        self.incursion_conditions_met = False

    def fail_incursion(self):
        self.incursion_starting_point = None
        self.current_incursion = []
        self.claiming = False
        self.incursion_conditions_met = False

    def is_claimed_point(self, x, y):
        i = 0
        while i < len(self.claimed_points):
            for point in self.claimed_points[i]:
                if point:
                    if point[0] == x and point[1] == y:
                        return True
                i += 1

        return False

    def offset(self, iterable):
        prev = None
        for elem in iterable:
            yield prev, elem
            prev = elem

    def margin_collision(self):
        if self.previous_move == 'left' and self.x == consts.MARGIN:
            return True
        elif self.previous_move == 'right' and self.x == consts.MAP_WIDTH - consts.MARGIN:
            return True
        elif self.previous_move == 'up' and self.y == consts.MARGIN:
            return True
        elif self.previous_move == 'down' and self.y == consts.MAP_HEIGHT - consts.MARGIN:
            return True
        else:
            return False

    def _change_in_incursion_direction(self, move):
        if (self.previous_move == 'up' or self.previous_move == 'down') and (move == 'right' or move == 'left') \
                and self.claiming:
            self.incursion_conditions_met = True
        elif (self.previous_move == 'right' or self.previous_move == 'left') and (move == 'up' or move == 'down') \
                and self.claiming:
            self.incursion_conditions_met = True
        else:
            pass

    def move(self, move: str):
        """ Controls the movement of the player """
        if self.claiming:
            self._claim_move(move)
        if not self.claiming:
            self._claimless_move(move)
        else:
            if self._opposite_movement(move): self._coordinate_move(move)

    def _opposite_movement(self, move):
        if move == self.previous_move:
            return True
        elif move == 'left' or move == 'right':
            return not (self.previous_move == 'left' or self.previous_move == 'right')
        elif move == 'up' or move == 'down':
            return not (self.previous_move == 'up' or self.previous_move == 'down')
        else:
            return True

    def _coordinate_move(self, move):

        self.previous_move = move

        if move == 'right':
            self._move_right()
        if move == 'left':
            self._move_left()
        if move == 'up':
            self._move_up()
        if move == 'down':
            self._move_down()

    def _simple_move(self, move):
        if move == 'right':
            self._move_right()
        if move == 'left':
            self._move_left()
        if move == 'up':
            self._move_up()
        if move == 'down':
            self._move_down()

    def _get_orientation(self):
        if (self.x == consts.MARGIN or self.x == consts.MAP_WIDTH - consts.MARGIN) and (self.y > consts.MARGIN):
            self.orientation = 'vertical'
        elif (self.y == consts.MARGIN or self.y == consts.MAP_WIDTH - consts.MARGIN) and (self.x > consts.MARGIN):
            self.orientation = 'horizontal'
        else:
            self.orientation = 'none'

    def _claimless_move(self, move):
        """ Handles the movement when player is not claiming areas"""
        self._get_orientation()

        if self.orientation == 'vertical' and (move == 'up' or move == 'down'):
            self._coordinate_move(move)
        elif self.orientation != 'vertical' and (move == 'right' or move == 'left'):
            self._coordinate_move(move)
        else:
            pass

    def _claim_move(self, move):
        """ Handles movement when player is claiming areas """
        if not self.current_incursion:
            self.incursion_starting_point = self.get_coordinate()
            self.add_incursion_point()
            self.previous_move = None

        if not self._opposite_movement(move):
            pass
        else:
            self._simple_move(move)
            self._change_in_incursion_direction(move)
            self.add_incursion_point()
            self.previous_move = move

            if self.margin_collision() and self.incursion_conditions_met:
                self.finish_incursion()
            elif self.margin_collision() and not self.incursion_conditions_met:
                self.fail_incursion()


    def _move_right(self):
        if self.x != consts.MAP_WIDTH - consts.MARGIN:
            self.x += consts.MOVE_DIM
        # elif self.is_claimed_point(self.x + consts.MOVE_DIM, self.y):
        #     self.x += consts.MOVE_DIM

    def _move_left(self):
        if self.x != consts.MARGIN:
            self.x -= consts.MOVE_DIM
        # elif self.is_claimed_point(self.x - consts.MOVE_DIM, self.y):
        #     self.x -= consts.MOVE_DIM

    def _move_up(self):
        if self.y != consts.MARGIN:
            self.y -= consts.MOVE_DIM
        # elif self.is_claimed_point(self.x, self.y - consts.MOVE_DIM):
        #     self.y -= consts.MOVE_DIM

    def _move_down(self):
        if self.y != consts.MAP_HEIGHT - consts.MARGIN:
            self.y += consts.MOVE_DIM
        # elif self.is_claimed_point(self.x, self.y + consts.MOVE_DIM):
        #     self.y += consts.MOVE_DIM


class Enemy:
    """ Manages the obstacles within the game """

    class _Qix:
        """ Implementing the logic for Qix Object. """

        def __init__(self):
            self.x, self.y = self._random_position()
            self.prev_move_x = None
            self.prev_move_y = None
            self.prev_move = None

        def _random_position(self):
            """ Generates a random position for qix """
            range_x = consts.MARGIN // consts.MOVE_DIM
            range_y = (consts.MAP_WIDTH - consts.MARGIN) // consts.MOVE_DIM

            x = random.randrange(range_x, range_y) * consts.MOVE_DIM
            y = random.randrange(range_x, range_y) * consts.MOVE_DIM

            return x, y

        def get_coordinate(self):
            return (self.x, self.y)

        def _next_move(self):
            self._possible_moves()

            self.prev_move = random.choice(self.moves)

            if self.prev_move == 'down':
                self._move_down()
            if self.prev_move == 'up':
                self._move_up()
            if self.prev_move == 'left':
                self._move_left()
            if self.prev_move == 'right':
                self._move_right()

            if self.prev_move == 'down' or self.prev_move == 'up':
                self.prev_move_y = self.prev_move
            if self.prev_move == 'left' or self.prev_move == 'right':
                self.prev_move_x = self.prev_move

        def _possible_moves(self):
            # Getting all the possible
            moves = []

            if self.x != consts.MARGIN:
                moves.append('left')
            if self.x != consts.MAP_WIDTH - consts.MARGIN:
                moves.append('right')
            if self.y != consts.MAP_HEIGHT - consts.MARGIN:
                moves.append('down')
            if self.y != consts.MARGIN:
                moves.append('up')

            # Optimize the randomness
            if random.randrange(0, 10) > 1:
                if "up" in moves and "down" in moves and len(moves) > 2:
                    if self.prev_move_y == "down":
                        moves.remove("up")
                    if self.prev_move_y == "up":
                        moves.remove("down")

                if "right" in moves and "left" in moves and len(moves) > 2:
                    if self.prev_move_x == "right":
                        moves.remove("left")
                    elif self.prev_move_x == "left":
                        moves.remove("right")

            self.moves = moves
            # print(self.moves, self.prev_move)

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

    class _Sparx:
        """ Implementing the logic for Sparx Object. """

        def __init__(self):
            self.move = None  # up, down, left, right of the grid
            self.x, self.y, self.orientation = self._random_position()
            self.change_move = False
            # print(self.x, self.y, self.orientation)

        def get_coordinate(self) -> (int, int):
            return self.x, self.y

        def get_orientation(self):
            return self.orientation

        def _random_position(self) -> (int, int):
            """ Return random positions for sparx """
            fix_x = [consts.MARGIN, consts.MAP_WIDTH - consts.MARGIN]
            fix_y = [consts.MARGIN, consts.MAP_HEIGHT - consts.MARGIN]

            range_x = consts.MARGIN // consts.MOVE_DIM
            range_y = (consts.MAP_WIDTH - consts.MARGIN) // consts.MOVE_DIM

            # 0: Vertical
            if random.choice([0, 1]) == 0:
                x = random.choice(fix_x)
                y = random.randrange(range_x, range_y) * consts.MOVE_DIM
                return x, y, 'vertical'
            else:
                x = random.randrange(range_x, range_y) * consts.MOVE_DIM
                y = random.choice(fix_y)
                return x, y, 'horizontal'

        def _next_move(self):
            # Check to see the orientation should change
            self._check_orientation()

            if self.move == None or self.change_move:
                self._initiate_move()
                self.change_move = False
                # print(self.move, self.orientation)

            if self.move == 'down':
                self._move_down()
            if self.move == 'up':
                self._move_up()
            if self.move == 'left':
                self._move_left()
            if self.move == 'right':
                self._move_right()

        def _initiate_move(self):
            if self.move == None:
                # Base cases: 4 points of the rectangle
                if self.x == consts.MARGIN and self.y == consts.MARGIN:
                    self.move = random.choice(['right', 'down'])
                if self.x == consts.MARGIN and self.y == consts.MAP_HEIGHT - consts.MARGIN:
                    self.move = random.choice(['right', 'up'])
                if self.x == consts.MAP_WIDTH - consts.MARGIN and self.y == consts.MARGIN:
                    self.move = random.choice(['left', 'down'])
                if self.x == consts.MAP_WIDTH - consts.MARGIN and self.y == consts.MAP_HEIGHT - consts.MARGIN:
                    self.move = random.choice(['left', 'up'])

                # 4 ranges
                if self.x == consts.MARGIN and self.y > consts.MARGIN or self.x == consts.MAP_WIDTH - consts.MARGIN and self.y > consts.MARGIN:
                    self.move = random.choice(["down", "up"])
                if self.x > consts.MARGIN and self.y == consts.MARGIN or self.x > consts.MARGIN and self.y == consts.MAP_HEIGHT - consts.MARGIN:
                    self.move = random.choice(["right", "left"])
            elif self.orientation == 'vertical':
                if (self.x == consts.MARGIN and self.y == consts.MARGIN) or (
                        self.x == consts.MAP_WIDTH - consts.MARGIN and self.y == consts.MARGIN):
                    self.move = "down"
                else:
                    self.move = 'up'
            else:
                if (self.x == consts.MARGIN and self.y == consts.MARGIN) or (
                        self.x == consts.MARGIN and self.y == consts.MAP_WIDTH - consts.MARGIN):
                    self.move = "right"
                else:
                    self.move = 'left'

        def _check_orientation(self):
            if self.orientation == 'vertical':
                if self.y == consts.MARGIN or self.y == consts.MAP_HEIGHT - consts.MARGIN:
                    self.orientation = 'horizontal'
                    self.change_move = True
            else:
                if self.x == consts.MARGIN or self.x == consts.MAP_HEIGHT - consts.MARGIN:
                    self.orientation = 'vertical'
                    self.change_move = True

        def _move_right(self):
            self.x += consts.MOVE_DIM

        def _move_left(self):
            self.x -= consts.MOVE_DIM

        def _move_up(self):
            self.y -= consts.MOVE_DIM

        def _move_down(self):
            self.y += consts.MOVE_DIM

    def __init__(self):
        self.quixes = []
        self.sparxes = []
        self.init = True

    def _add_sparx(self):
        self.sparxes.append(Enemy._Sparx())

    def _add_qix(self):
        self.quixes.append(Enemy._Qix())

    def update(self):
        if self.init:
            self._add_qix()
            self._add_sparx()
            self.init = False

        self._fetch_next_moves()

    def _fetch_next_moves(self):
        for sparx in self.sparxes:
            sparx._next_move()

        for quix in self.quixes:
            quix._next_move()


def get_last_outer_point(points_list):
    """ Gets 2 points to make a straight line down """
    i = 0
    start_point = points_list[i]
    width_of_incursion = points_list[-1][0] - start_point[0]
    end_point = None
    for point_a, point_b in points_list:
        if point_a and point_b:
            if point_a[0] == point_b[0] and point_a[1] + consts.MOVE_DIM == point_b[1]:
                end_point = point_b
            elif point_a[0] == point_b[0] and point_a[1] - consts.MOVE_DIM == point_b[1]:
                end_point = point_b
            else:
                end_point = point_a

    return True


def get_head_and_tail(a_list):
    head = a_list[0]
    tail = a_list[-1]
    return head, tail


def find_displacement_in_list(points_list):
    """ Given a list of points, finds the x and y displacement """
    head, tail = get_head_and_tail(points_list)
    x_displacement = tail[0] - head[0]
    y_displacement = tail[1] - head[1]
    return x_displacement, y_displacement


def _determine_qix_direction(qix: Enemy._Qix, claimed_list):
    """ Returns the direction of the Qix relative to the incursion made by the player """
    qix_coordinates = qix.get_coordinate()
    direction = None
    if _is_qix_above_claimed_area(qix_coordinates, claimed_list):
        direction = "above"
    elif _is_qix_below_claimed_area(qix_coordinates, claimed_list):
        direction = "below"
    elif _is_qix_right_claimed_area(qix_coordinates, claimed_list):
        direction = "right"
    elif _is_qix_left_claimed_area(qix_coordinates, claimed_list):
        direction = "left"
    else:
        # None means that the Qix is inside the rectangle.
        direction = "none"

    return direction


def _is_qix_below_claimed_area(qix_coordinates, points_list):
    """ Returns true if the Qix is below all the points in the incursion """
    for point in points_list:
        if point[1] >= qix_coordinates[1]:
            return False

    return True


def _is_qix_above_claimed_area(qix_coordinates, points_list):
    """ Returns true if the Qix is above all the points in the incursion """
    for point in points_list:
        if point[1] <= qix_coordinates[1]:
            return False

    return True


def _is_qix_right_claimed_area(qix_coordinates, points_list):
    """ Returns true if the Qix is to the right all the points in the incursion """
    for point in points_list:
        if point[0] >= qix_coordinates[0]:
            return False

    return True


def _is_qix_left_claimed_area(qix_coordinates, points_list):
    """ Returns true if the Qix is to the left all the points in the incursion """
    for point in points_list:
        if point[0] <= qix_coordinates[0]:
            return False

    return True


class Map:
    """ Main map that renders everything within here """

    def __init__(self, height: int = consts.MAP_HEIGHT, width: int = consts.MAP_WIDTH):
        self.width = width
        self.height = height

        # Initialize the pygame module
        pygame.init()

        self.life = Text()

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
        self._draw_player_claimed_areas()
        self._draw_current_incursion()
        self._draw_player()

        self.enemy.update()
        self._render_enemy()

        # Write the  text
        # Note: This should be rendered at the end to overwrite anything else!
        self.gameDisplay.blit(self.life.get_text(), self.life.get_coordinate())

    def _render_enemy(self):
        """ Renders the graphics for enemy objects. """
        for sparx in self.enemy.sparxes:
            self._draw_sparx(sparx)

        for quix in self.enemy.quixes:
            self._draw_qix(quix)

    def _draw_sparx(self, sparx: Enemy._Sparx, color=consts.SPARX_COLOR):
        x, y = sparx.get_coordinate()

        pygame.draw.polygon(self.gameDisplay,
                            color,
                            [(x, y - consts.SPARX_DIM), (x + consts.SPARX_DIM, y),
                             (x, y + consts.SPARX_DIM), (x - consts.SPARX_DIM, y)])

    def _draw_qix(self, quix: Enemy._Qix, color=consts.QIX_COLOR):
        x, y = quix.get_coordinate()

        pygame.draw.polygon(self.gameDisplay,
                            consts.QIX_COLOR,
                            [(x, y - consts.QIX_DIM), (x + consts.QIX_DIM, y),
                             (x, y + consts.QIX_DIM), (x - consts.QIX_DIM, y)])

    def _fill_normal(self, points_list):
        x_displacement, y_displacement = find_displacement_in_list(points_list)
        points_start, points_end = get_head_and_tail(points_list)
        rectangle_width, rectangle_height = self.player.get_incursion_dimensions(points_list)
        if x_displacement < 0 and y_displacement < 0:
            """ Moved left and up to create the rectangle """
            rectangle = pygame.Rect(points_end[0], points_end[1], rectangle_width, rectangle_height)
        elif x_displacement > 0 and y_displacement < 0:
            """ Moved right and up to create the rectangle """
            rectangle = pygame.Rect(points_start[0], points_start[1] - rectangle_height, rectangle_width, rectangle_height)
        elif x_displacement < 0 and y_displacement > 0:
            """ Moved left and down to create the rectangle """
            rectangle = pygame.Rect(points_end[0], points_end[1] - rectangle_height, rectangle_width, rectangle_height)
        else:
            """ Moved right and down to create the rectangle """
            rectangle = pygame.Rect(points_start[0], points_start[1], rectangle_width, rectangle_height)

        pygame.draw.rect(self.gameDisplay, consts.CLAIMED_AREA_COLOR, rectangle)
        pygame.draw.rect(self.gameDisplay, consts.BORDER_COLOR, rectangle, 1)

    def _fill_all_else(self, points_list):
        x_displacement, y_displacement = find_displacement_in_list(points_list)
        points_start, points_end = get_head_and_tail(points_list)
        rectangle_width, rectangle_height = self.player.get_incursion_dimensions(points_list)
        rectangle_map_area = pygame.Rect(consts.MARGIN, consts.MARGIN, 380, 380)
        if x_displacement < 0 and y_displacement < 0:
            """ Moved left and up to create the rectangle """
            rectangle = pygame.Rect(points_end[0], points_end[1], rectangle_width, rectangle_height)
        elif x_displacement > 0 and y_displacement < 0:
            """ Moved right and up to create the rectangle """
            rectangle = pygame.Rect(points_start[0], points_start[1] - rectangle_height, rectangle_width,
                                    rectangle_height)
        elif x_displacement < 0 and y_displacement > 0:
            """ Moved left and down to create the rectangle """
            rectangle = pygame.Rect(points_end[0], points_end[1] - rectangle_height, rectangle_width, rectangle_height)
        else:
            """ Moved right and down to create the rectangle """
            rectangle = pygame.Rect(points_start[0], points_start[1], rectangle_width, rectangle_height)

        pygame.draw.rect(self.gameDisplay, consts.CLAIMED_AREA_COLOR, rectangle_map_area)
        pygame.draw.rect(self.gameDisplay, consts.BORDER_COLOR, rectangle_map_area, 1)
        pygame.draw.rect(self.gameDisplay, consts.BG_COLOR, rectangle)
        pygame.draw.rect(self.gameDisplay, consts.BORDER_COLOR, rectangle, 1)

    def _fill_player_claimed_areas(self, current_claim_segment):
        """ Fill the player claimed area relative to the qix's location """
        qix_direction = _determine_qix_direction(self.enemy.quixes[0], current_claim_segment)
        if qix_direction == "none":
            self._fill_all_else(current_claim_segment)
            self.player.update_total_claimed_area_qix_inside(current_claim_segment)
        else:
            self._fill_normal(current_claim_segment)

    def _draw_player_claimed_borders(self, current_claim_segment):
        for point_a, point_b in self.player.offset(current_claim_segment):
            if point_a and point_b:
                pygame.draw.line(self.gameDisplay, consts.BORDER_COLOR, (point_a[0], point_a[1]),
                                 (point_b[0], point_b[1]), 1)

    def _draw_player_claimed_areas(self):
        i = 0
        while i < len(self.player.claimed_points):
            if self.player.claimed_points[i]:
                current_points_list = self.player.claimed_points[i]
                self._draw_player_claimed_borders(current_points_list)
                self._fill_player_claimed_areas(current_points_list)
            i += 1

    def _draw_current_incursion(self):
        for point_a, point_b in self.player.offset(self.player.current_incursion):
            if point_a and point_b:
                if not self.player.incursion_conditions_met:
                    pygame.draw.line(self.gameDisplay, consts.INCURSION_BAD_COLOR, (point_a[0], point_a[1]),
                                     (point_b[0], point_b[1]), 1)
                else:
                    pygame.draw.line(self.gameDisplay, consts.INCURSION_GOOD_COLOR, (point_a[0], point_a[1]),
                                     (point_b[0], point_b[1]), 1)

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


def run():
    # Initialization
    clock = pygame.time.Clock()
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
                    map.player.claiming = True

                # Pausing
                if event.key == pygame.K_p:
                    PAUSE = not PAUSE

                # Moving Manually
                if event.key == pygame.K_RIGHT:
                    map.player.move("right")

                if event.key == pygame.K_LEFT:
                    map.player.move("left")

                if event.key == pygame.K_UP:
                    map.player.move("up")

                if event.key == pygame.K_DOWN:
                    map.player.move("down")

        # If the game is not paused then render the graphics
        if not PAUSE:
            map.render()

        pygame.display.update()
        clock.tick(consts.FPS)
