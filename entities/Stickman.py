import pygame

WHITE = "white"

class Stickman(pygame.sprite.Sprite):
    def __init__(self, x = 100, y = 500, color=(255,0,0)):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
