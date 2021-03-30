import pygame

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

class PlayerPath:
    pass

class Player:
    pass

class Quark:
    pass

class Map:
    def __init__(self):
        pass

    def render(self):
        # Instantiating the initial properties for the application
        pygame.init()
        # Setting the height and width
        self.gameDisplay = pygame.display.set_mode((400, 400))
        self.gameDisplay.fill((245,235,235))
        # Setting the caption
        pygame.display.set_caption('QIX')

        # pygame.draw.rect(self.gameDisplay, (0,10,10), (20, 20, 280, 280))
        # Initializing the pixel property
        self.pixel = pygame.PixelArray(self.gameDisplay)
        self.draw_borders()
        
    def draw_borders(self, thick=2, margin=30, color=(0, 0, 0)):
        x1, x2 = margin, 400 - margin
        y1, y2 = 30, 30 + thick

        self.pixel[x1:x2, y1:y2] = (0, 0, 0)
        self.pixel[y1:y2, x1:x2] = (0, 0, 0)

        self.pixel[x1:x2, x2:x2+thick] = (0, 0, 0)
        self.pixel[x2:x2+thick, x1:x2] = (0, 0, 0)


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
