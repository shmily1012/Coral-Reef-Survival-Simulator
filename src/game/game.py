import pygame
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill("black")
            pygame.display.flip()

