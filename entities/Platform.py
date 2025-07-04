import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        # Top left just says the corresponding rectangle created from the surface starts at x, y
        self.rect = self.image.get_rect(topleft=(x, y))
