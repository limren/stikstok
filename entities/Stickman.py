import pygame

WHITE = (255, 255, 255)

class Stickman(pygame.sprite.Sprite):
    def __init__(self, x = 100, y = 500, color=(255,0,0)):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_alive = False
        self.speed = pygame.math.Vector2(3, 3)

    def update(self, platforms_group):
        collisions = self.check_collisions(platforms_group)

        if not collisions["bottom"]:
            self.rect.y += self.speed.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not collisions["left"]:
            self.rect.x -= self.speed.x
        if keys[pygame.K_RIGHT] and not collisions["right"]:
            self.rect.x += self.speed.x


    def check_collisions(self, platforms_group):
        collisions = {"left": False, "right": False, "top": False, "bottom": False}

        left_rect = self.rect.move(-self.speed.x, 0)
        right_rect = self.rect.move(self.speed.x, 0)
        top_rect = self.rect.move(0, -self.speed.y)
        bottom_rect = self.rect.move(0, self.speed.y)

        for platform in platforms_group:
            if platform.rect.colliderect(left_rect):
                collisions["left"] = True
            if platform.rect.colliderect(right_rect):
                collisions["right"] = True
            if platform.rect.colliderect(top_rect):
                collisions["top"] = True
            if platform.rect.colliderect(bottom_rect):
                collisions["bottom"] = True

        return collisions
