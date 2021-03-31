import pygame
import consts

class Point:
    """
        Point Object storing the properties and attributes
        of a pixel within the pixelArray.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.passer = []

    def add_passer(self, passer):
        self.passer.append(passer)

class Player:
    def __init__(self):
        self.points = []

    def add_point(self, point: Point):
        self.points.append(point)

class Map:
    def __init__(self, height=420, width=420):
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

    def render(self):
        """ Renders the graphics """

        self.gameDisplay.fill(consts.BG_COLOR)

        # Draw the borders
        self._draw_borders()

    def _draw_player(self):
        """ Draws the player """
        pass
        
    def _draw_borders(self, thick=2, margin=20, color=(0, 0, 0)):
        """ Draws the border for the QIX game """
        self.pixel[margin: self.width - margin, margin:margin+thick] = color # Upper Horizontal Line
        self.pixel[margin: self.width - margin, self.height - margin:self.height - margin + thick] = color # Lower Horizontal Line
        self.pixel[margin: margin+thick, margin:self.height - margin] = color # Left Vertical Line
        self.pixel[self.width - margin:self.width - margin + thick, margin:self.height - margin] = color # Right Vertical Line


map = Map()
map.render()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: print("l")
            if event.key == pygame.K_r: print("s")                
            if event.key == pygame.K_x:  print("ss")

    pygame.display.update()
