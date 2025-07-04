# Example file showing a basic pygame "game loop"
import pygame
from entities.Stickman import Stickman
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
WHITE = "white"

player_one = Stickman()
players_group = pygame.sprite.Group()
players_group.add(player_one)

platform_rec = pygame.Rect(0, screen.get_height() - 100, screen.get_width(), 100)
#platform_rect_pos = pygame.Vector2(screen.get_width(), 50)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # RENDER YOUR GAME HERE
    players_group.draw(screen)
    pygame.draw.rect(screen, "white", platform_rec)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
