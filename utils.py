import consts
import pygame
import random
import time

global border_points
# This global entity should be used to draw borders and restrict movement
border_points = [
    (consts.MARGIN, consts.MARGIN),
    (consts.MAP_DIM - consts.MARGIN, consts.MARGIN),
    (consts.MAP_DIM - consts.MARGIN, consts.MAP_DIM - consts.MARGIN),
    (consts.MARGIN, consts.MAP_DIM - consts.MARGIN)]

# Some of the repeated constants:
fix_x = [consts.MARGIN, consts.MAP_DIM - consts.MARGIN]
fix_y = [consts.MARGIN, consts.MAP_DIM - consts.MARGIN]

range_x = consts.MARGIN // consts.MOVE_DIM
range_y = (consts.MAP_DIM - consts.MARGIN) // consts.MOVE_DIM


class Point:
    """ Storing Point information """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.adj_vertices = []
        self.direction_change = False
        # Horizontal and Vertical adjacencies
        self.h_adj, self.v_adj = [], []

    def get_coordinate(self) -> (int, int):
        return (self.x, self.y)


class Border:
    """ Connect points """

    def __init__(self):
        self.points: [Point] = []
        self.player_border = border_points
        # Each element will have 2 coordinates indicating a claimed area
        self.claim_points = []

        self._initiate()

    def _initiate(self):
        """ Initiales the  border. """
        for x1, y1 in border_points:
            point = Point(x1, y1)

            for x2, y2 in border_points:
                if (x1, y1) != (x2, y2):
                    if x2 == x1:
                        point.v_adj.append((x2, y2))

                    if y2 == y1:
                        point.h_adj.append((x2, y2))

            self.points.append(point)

    def add_border_points(self, points: [(int, int)]):
        # Relate the new points
        self._relate_new_points(points)
        # Update the adjacencies
        self._update_adjacencies()

        for point in self.points:
            print(f'{point.get_coordinate()} ', end='')
        print()

        print(f'claimed: {self.claim_points}')

    def _relate_new_points(self, points):
        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]

            p1 = Point(x1, y1)
            p2 = Point(x2, y2)

            p1.h_adj, p1.v_adj = self._relate_to_border(x1, y1)
            p2.h_adj, p2.v_adj = self._relate_to_border(x2, y2)

            if x1 == x2:
                p1.v_adj.append((x2, y2))
                p2.v_adj.append((x1, y1))

                left, top = min(x1, x2), min(y1, y2)

                self.claim_points.append((left, 
                                        top, 
                                        abs(400 - left), 
                                        abs(400 - top)))
            else:
                p1.h_adj.append((x2, y2))
                p2.h_adj.append((x1, y1))
                
                left, top = min(x1, x2), min(y1, y2)

                self.claim_points.append((left, 
                                        top, 
                                        abs(400 - left), 
                                        abs(400 - top)))

            self.points.append(p1)
            self.points.append(p2)
        else:
            for i in range(len(points) - 2):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                x3, y3 = points[i + 2]

                left, top = min(x1, x2, x3), min(y1, y2, y3)

                if i != len(points) - 3:
                    self.claim_points.append((left, 
                                        top, 
                                        abs(400 - left),
                                        abs(400 - top)
                                        ))

                p2 = Point(x2, y2)

                # Adding the first point
                if i == 0:
                    p1 = Point(x1, y1)
                    p1.h_adj, p1.v_adj = self._relate_to_border(x1, y1)
                    if x2 == x1:
                        p1.v_adj.append((x2, y2))
                    if y2 == y1:
                        p1.h_adj.append((x2, y2))
                    self.points.append(p1)

                # Adding the last point
                if i == len(points) - 3:
                    last_point = Point(x3, y3)
                    last_point.h_adj, last_point.v_adj = self._relate_to_border(
                        x3, y3)
                    if x2 == x3:
                        last_point.v_adj.append((x2, y2))
                    if y2 == y3:
                        last_point.h_adj.append((x2, y2))
                    self.points.append(last_point)

                # Dealing with the middle point
                if x2 == x1:
                    p2.v_adj.append((x1, y1))
                if y2 == y1:
                    p2.h_adj.append((x1, y1))
                if x2 == x3:
                    p2.v_adj.append((x3, y3))
                if y2 == y3:
                    p2.h_adj.append((x3, y3))
                self.points.append(p2)

    def _relate_to_border(self, x, y):
        """ Relates the first and last new points to 
        the old border points """
        h, v = [], []

        for point in self.points:
            if point.x == x:
                v.append(point.get_coordinate())
                point.v_adj.append((x, y))
                point.v_adj.sort()

            if point.y == y:
                h.append(point.get_coordinate())
                point.h_adj.append((x, y))
                point.h_adj.sort()
    
        h.sort()
        v.sort()
        return h, v

    # This function is problematic
    def _update_adjacencies(self):
        """
            The initial border points can have one horizontal and 
            one vertical adjacent vertices.

            However, the rest of the border points that are added
            afterwards can have two of each adjacent vertex type.
        """
        for point in self.points:
            # print(f'p:{point.get_coordinate()}, h: {point.h_adj}, v:{point.v_adj}')
            if point.get_coordinate() in border_points:
                # Initial Border point update
                # The last element (newly added point should be the onlt adjacency)
                if len(point.h_adj) > 1:
                    closest = point.h_adj[0]
                    for x, y in point.h_adj:
                        if abs(point.x - x) < abs(point.x - closest[0]):
                            closest = (x, y)
                    point.h_adj = [closest]

                if len(point.v_adj) > 1:
                    closest = point.v_adj[0]
                    for x, y in point.v_adj:
                        if abs(point.y - y) < abs(point.y - closest[1]):
                            closest = (x, y)
                    point.v_adj = [closest]
            else:
                if len(point.h_adj) > 2:
                    last = point.h_adj[-1]
                    p1 = point.h_adj[0]
                    p2 = point.h_adj[1]

                    if p1 < last and last < p2:
                        point.h_adj.remove(p1)
                    else:
                        point.h_adj.remove(p2)

                if len(point.v_adj) > 2:
                    last = point.v_adj[-1]
                    p1 = point.v_adj[0]
                    p2 = point.v_adj[1]

                    if p1 < last and last < p2:
                        point.v_adj.remove(p1)
                    else:
                        point.v_adj.remove(p2)

            print(f'p:{point.get_coordinate()}, h: {point.h_adj}, v:{point.v_adj}')

    def on_border(self, x: int, y: int) -> bool:
        """ Checks to see if a given point is on the border or not. """
        for point in self.points:
            px, py = point.get_coordinate()

            for x2, y2 in point.h_adj:
                if py == y:
                    bx, sx = self._sort(px, x2)

                    if x >= sx and x <= bx:
                        return True

            for x2, y2 in point.v_adj:
                if px == x:
                    by, sy = self._sort(py, y2)

                    if y >= sy and y <= by:
                        return True
        return False

    def _sort(self, val1, val2):
        if val1 < val2:
            return val2, val1

        return val1, val2

    def out_border(self, x, y):
        """ Given the points it determines if the move will go beyond the borders or not? """
        pass


class Text:
    """ Lives and claimed area text """

    def __init__(self, initial_life: int = consts.INIT_LIFE):
        pygame.font.init()
        self.life = initial_life
        self.font = pygame.font.SysFont('Comic Sans MS', consts.FONT_SIZE)

        self.claimed_percentage = 0

    def update(self, new_life):
        self.life = new_life

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
        self.x = (consts.MAP_DIM - consts.MARGIN) // 2
        self.y = consts.MAP_DIM - consts.MARGIN
        self.claiming = False
        self.previous_move = None
        self.life_force = 10

        self._left_border = False

        # Claimed areas will be rendered via this list
        self.claimed_points = []
        self.current_incursion = []

    def get_coordinate(self):
        return (self.x, self.y)

    def reset_points(self):
        self.points = []
        self._left_border = False
        self.claiming = False

    def move(self, move: str):
        """ Controls the movement of the player """
        self._leave_border(move)

        if self.claiming and self._left_border:
            if self._opposite_movement(move):
                self._coordinate_move(move)
        else:
            self._claimless_move(move)

    def _opposite_movement(self, move):
        if move == self.previous_move:
            return True
        elif move == 'left' or move == 'right':
            return not (self.previous_move == 'left' or self.previous_move == 'right')
        elif move == 'up' or move == 'down':
            return not (self.previous_move == 'up' or self.previous_move == 'down')
        else:
            return True

    def _leave_border(self, move):
        if self._left_border:
            pass
        else:
            self._get_orientation()

            if self.orientation == 'vertical' and (move == "right" or move == "left"):
                self._left_border = True
            elif self.orientation != 'vertical' and (move == "down" or move == "up"):
                self._left_border = True
            else:
                self._left_border = False

    def _coordinate_move(self, move):
        if self.previous_move != move and self._left_border:
            self.points.append((self.x, self.y))
            # print(self.points)

        self.previous_move = move

        if move == 'right':
            self._move_right()
        if move == 'left':
            self._move_left()
        if move == 'up':
            self._move_up()
        if move == 'down':
            self._move_down()

    def _get_orientation(self):
        if (self.x == consts.MARGIN or self.x == consts.MAP_DIM - consts.MARGIN) and (self.y > consts.MARGIN):
            self.orientation = 'vertical'
        elif (self.y == consts.MARGIN or self.y == consts.MAP_DIM - consts.MARGIN) and (self.x > consts.MARGIN):
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

    def _move_right(self):
        if self.x != consts.MAP_DIM - consts.MARGIN:
            self.x += consts.MOVE_DIM

    def _move_left(self):
        if self.x != consts.MARGIN:
            self.x -= consts.MOVE_DIM

    def _move_up(self):
        if self.y != consts.MARGIN:
            self.y -= consts.MOVE_DIM

    def _move_down(self):
        if self.y != consts.MAP_DIM - consts.MARGIN:
            self.y += consts.MOVE_DIM


class Enemy:
    """ Manages the obstacles within the game """

    class _Qix:
        """ Implementing the logic for Qix Object. """

        def __init__(self):
            self.x, self.y = self._random_position()
            self.prev_move_x = None
            self.prev_move_y = None
            self.prev_move = None
            self.collision = None

        def _random_position(self):
            """ Generates a random position for qix """

            x = random.randrange(range_x, range_y) * consts.MOVE_DIM
            y = random.randrange(range_x, range_y) * consts.MOVE_DIM

            return x, y

        def get_coordinate(self):
            return (self.x, self.y)

        def get_mapping(self):
            return [(self.x, self.y - consts.QIX_DIM),
                    (self.x + consts.QIX_DIM, self.y),
                    (self.x, self.y + consts.QIX_DIM),
                    (self.x - consts.QIX_DIM, self.y)]

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

            if self.x != consts.MARGIN + consts.QIX_DIM:
                moves.append('left')
            if self.x != consts.MAP_DIM - consts.MARGIN - consts.QIX_DIM:
                moves.append('right')
            if self.y != consts.MAP_DIM - consts.MARGIN - consts.QIX_DIM:
                moves.append('down')
            if self.y != consts.MARGIN + consts.QIX_DIM:
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
            if self.x != consts.MAP_DIM - consts.MARGIN:
                self.x += consts.MOVE_DIM

        def _move_left(self):
            if self.x != consts.MARGIN:
                self.x -= consts.MOVE_DIM

        def _move_up(self):
            if self.y != consts.MARGIN:
                self.y -= consts.MOVE_DIM

        def _move_down(self):
            if self.y != consts.MAP_DIM - consts.MARGIN:
                self.y += consts.MOVE_DIM

    class _Sparx:
        """ Implementing the logic for Sparx Object. """

        def __init__(self):
            self.move = None  # up, down, left, right of the grid
            self.x, self.y, self.orientation = self._random_position()
            self.change_move = False
            self.collision = None

        def get_coordinate(self) -> (int, int):
            return self.x, self.y

        def get_orientation(self):
            return self.orientation

        def get_mapping(self):
            return [(self.x, self.y - consts.SPARX_DIM),
                    (self.x + consts.SPARX_DIM, self.y),
                    (self.x, self.y + consts.SPARX_DIM),
                    (self.x - consts.SPARX_DIM, self.y)]

        def _random_position(self) -> (int, int):
            """ Return random positions for sparx """

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
                if self.x == consts.MARGIN and self.y == consts.MAP_DIM - consts.MARGIN:
                    self.move = random.choice(['right', 'up'])
                if self.x == consts.MAP_DIM - consts.MARGIN and self.y == consts.MARGIN:
                    self.move = random.choice(['left', 'down'])
                if self.x == consts.MAP_DIM - consts.MARGIN and self.y == consts.MAP_DIM - consts.MARGIN:
                    self.move = random.choice(['left', 'up'])

                # 4 ranges
                if self.x == consts.MARGIN and self.y > consts.MARGIN or self.x == consts.MAP_DIM - consts.MARGIN and self.y > consts.MARGIN:
                    self.move = random.choice(["down", "up"])
                if self.x > consts.MARGIN and self.y == consts.MARGIN or self.x > consts.MARGIN and self.y == consts.MAP_DIM - consts.MARGIN:
                    self.move = random.choice(["right", "left"])
            elif self.orientation == 'vertical':
                if (self.x == consts.MARGIN and self.y == consts.MARGIN) or (
                        self.x == consts.MAP_DIM - consts.MARGIN and self.y == consts.MARGIN):

                    self.move = "down"
                else:
                    self.move = 'up'
            else:
                if (self.x == consts.MARGIN and self.y == consts.MARGIN) or (
                        self.x == consts.MARGIN and self.y == consts.MAP_DIM - consts.MARGIN):

                    self.move = "right"
                else:
                    self.move = 'left'

        def _check_orientation(self):
            if self.orientation == 'vertical':
                if self.y == consts.MARGIN or self.y == consts.MAP_DIM - consts.MARGIN:
                    self.orientation = 'horizontal'
                    self.change_move = True
            else:
                if self.x == consts.MARGIN or self.x == consts.MAP_DIM - consts.MARGIN:
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

        self.t1 = time.time()

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

        # After some time add a Sparx
        if 9.6 < time.time() - self.t1 < 10:
            self._add_sparx()

    def _fetch_next_moves(self):
        for sparx in self.sparxes:
            sparx._next_move()

        for quix in self.quixes:
            quix._next_move()

    def _check_collisions(self, player):
        # Returns True if collision with qix or sparx
        incursion = player.current_incursion
        player_coordinate = player.get_coordinate()

        if len(incursion) > 0:
            for qix in self.quixes:
                x, y = qix.get_coordinate()
                for point in incursion:
                    if [x, y] == point:
                        qix.collision = True
                        return True
                    else:
                        qix.collision = False

        for sparx in self.sparxes:
            if sparx.get_coordinate() == player_coordinate:
                sparx.collision = True
                return True
            else:
                sparx.collision = False

        return False

    def _respawn(self):
        for qix in self.quixes:
            qix.x, qix.y = qix._random_position()

        for sparx in self.sparxes:
            sparx.x, sparx.y, sparx.orientation = sparx._random_position()
            sparx._check_orientation()
            sparx.change_move = True


class Collision:
    """ Handles collisions """

    def __init__(self, player: Player, quixes: [Enemy._Qix], sparxes: [Enemy._Sparx]):
        self.player = player
        self.quixes = quixes
        self.sparxes = sparxes


class Map:
    """ Main map that renders graphics """

    def __init__(self, height: int = consts.MAP_DIM, width: int = consts.MAP_DIM, margin: int = consts.MARGIN):
        # Set the dimension of the square
        self.dim = width

        pygame.init()  # Initialize the pygame module
        self.text = Text()  # Text of the game
        self.border = Border()  # The dynamic Bordering
        self.player = Player()  # The player Object
        self.enemy = Enemy()  # The enmy object

        # Set the properties of the game Display
        self.gameDisplay = pygame.display.set_mode((self.dim, self.dim))
        self.gameDisplay.fill(consts.BG_COLOR)

        # Setting the caption
        pygame.display.set_caption('QIX')

    def start_claiming(self):
        self.player.claiming = True

    def render(self):
        # Fill the background color
        self.gameDisplay.fill(consts.BG_COLOR)

        # Drawing the claimed areas
        self._draw_claimed_areas()

        # Draw the player and the claimed areas
        self._draw_player()

        # Draw the enemy
        self._render_enemy()

        if self.enemy._check_collisions(self.player):
            self._handle_collision(self.player)

        # Write the  text
        # Note: This should be rendered at the end to overwrite anything else!
        self.gameDisplay.blit(self.text.get_text(), self.text.get_coordinate())
        # Draw the borders
        self._draw_borders()

    def _handle_collision(self, player):
        self._update_life(player)
        self._draw_player()
        self._render_enemy()

    def move_player(self, move):
        self.player.move(move)

        x, y = self.player.get_coordinate()

        # print(f'player: {self.player.get_coordinate()}, onBorder: {self.border.on_border(x, y)}, cl: {self.player.claiming}, l: {self.player._left_border}')

        if self.border.on_border(x, y) and self.player.claiming:
            self.player.points.append((x, y))
            print(self.player.points)
            self.border.add_border_points(self.player.points)
            self.player.reset_points()

    def _draw_claimed_areas(self):
        for coordinates in self.border.claim_points:
            pygame.draw.rect(surface=self.gameDisplay, 
                            color=consts.INCURSION_GOOD_COLOR,
                            rect=coordinates
                            )

    def _render_enemy(self):

        # Update enemy before rendering its properties
        self.enemy.update()

        for sparx in self.enemy.sparxes:
            self._draw_sparx(sparx)

        for quix in self.enemy.quixes:
            self._draw_qix(quix)

    def _draw_sparx(self, sparx: Enemy._Sparx, color=consts.SPARX_COLOR):
        pygame.draw.polygon(self.gameDisplay,
                            color,
                            sparx.get_mapping())

    def _draw_qix(self, quix: Enemy._Qix, color=consts.QIX_COLOR):
        pygame.draw.polygon(self.gameDisplay,
                            consts.QIX_COLOR,
                            quix.get_mapping())

    def _draw_player(self):
        pygame.draw.circle(self.gameDisplay,
                           consts.PLAYER_COLOR,
                           self.player.get_coordinate(),
                           consts.PLAYER_RADIUS)

    def _draw_borders(self, margin: int = consts.MARGIN, color: (int, int, int) = consts.BORDER_COLOR):
        for point in self.border.points:
            start_point = point.get_coordinate()

            for adj_vertex in point.h_adj:
                pygame.draw.line(self.gameDisplay,
                                 color,
                                 start_point, adj_vertex)

            for adj_vertex in point.v_adj:
                pygame.draw.line(self.gameDisplay,
                                 color,
                                 start_point, adj_vertex)

        if len(self.player.points) != 0:
            self._draw_temp_claim_lines()

    def _draw_temp_claim_lines(self):
        for index in range(0, len(self.player.points) - 1):
            pygame.draw.line(self.gameDisplay,
                             consts.BORDER_COLOR,
                             self.player.points[index], self.player.points[index + 1])

        pygame.draw.line(self.gameDisplay,
                         consts.BORDER_COLOR,
                         self.player.points[-1], self.player.get_coordinate())

    def _update_life(self, player):
        for qix in self.enemy.quixes:
            if qix.collision:
                self.text.update('Qix')
                qix.collision = False
                player.reposition()
                self.enemy._respawn()
                return

        for sparx in self.enemy.sparxes:
            if sparx.collision:
                self.text.update('Sparx')
                sparx.collision = False
                self.enemy._respawn()
                return


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
                    map.start_claiming()

                # Pausing
                if event.key == pygame.K_p:
                    PAUSE = not PAUSE

                # Moving Manually
                if event.key == pygame.K_RIGHT:
                    map.move_player("right")

                if event.key == pygame.K_LEFT:
                    map.move_player("left")

                if event.key == pygame.K_UP:
                    map.move_player("up")

                if event.key == pygame.K_DOWN:
                    map.move_player("down")

        # If the game is not paused then render the graphics
        if not PAUSE:
            map.render()

        pygame.display.update()
        clock.tick(consts.FPS)
