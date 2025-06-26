import pygame

class Canvas:
    def __init__(self, width = 800, height = 600):
        self.WIDTH = width
        self.HEIGHT = height

        self.screen = None
        self.clock = None
        self.font = None

        #inits screen, clock, font values
        self.init()
    
    def init(self):
        pygame.init()
        pygame.display.set_caption("Pong GA")
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)