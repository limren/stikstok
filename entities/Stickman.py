import pygame

WHITE = (255, 255, 255)

class Stickman(pygame.sprite.Sprite):
    def __init__(self, x=100, y=500, color=(255, 0, 0)):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel = pygame.math.Vector2(0, 0)
        self.speed_x = 3
        self.gravity = 0.5
        self.jump_strength = -10
        self.max_fall_speed = 10
        self.is_grounded = False

    def update(self, platforms_group):
        keys = pygame.key.get_pressed()

        # Velocity on horizontal movement, doesn't increase or decrease since no gravity is applied to horizontal movements
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed_x
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.speed_x

        # When falling
        self.vel.y += self.gravity
        if self.vel.y > self.max_fall_speed:
            self.vel.y = self.max_fall_speed

        # Jumping
        if keys[pygame.K_UP] and self.is_grounded:
            self.vel.y = self.jump_strength
        self.check_collision_x(platforms_group)

        self.rect.y += self.vel.y
        self.check_collision_y(platforms_group)

    def check_collision_x(self, platforms_group):
        # For each platform, we check if there's a collision on left and right sides (horizontal movements), if so, we put our player to the side of the platform
        for platform in platforms_group:
            if self.rect.colliderect(platform.rect):
                if self.vel.x > 0:  # moving right
                    self.rect.right = platform.rect.left
                elif self.vel.x < 0:  # moving left
                    self.rect.left = platform.rect.right

    def check_collision_y(self, platforms_group):
        self.is_grounded = False
        for platform in platforms_group:
            if self.rect.colliderect(platform.rect):
                if self.vel.y > 0:  # falling
                    self.rect.bottom = platform.rect.top
                    self.vel.y = 0
                    self.is_grounded = True
                elif self.vel.y < 0:  # jumping up
                    self.rect.top = platform.rect.bottom
                    self.vel.y = 0

