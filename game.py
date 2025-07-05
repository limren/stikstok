# Example file showing a basic pygame "game loop"
import pygame
from entities.Stickman import Stickman
from entities.Platform import Platform
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
WHITE = (255, 255, 255)

player_one = Stickman()
players_group = pygame.sprite.Group()
players_group.add(player_one)

## Simple platforms chunk for now
platforms_spec = [
    (0, screen.get_height() - 40, screen.get_width(), 40),
    (screen.get_width() / 5, screen.get_height() - 80, screen.get_width() / 5, 80),

    #(100, screen.get_height() - 140, 180, 20),
    #(350, screen.get_height() - 200, 160, 20),
    #(600, screen.get_height() - 260, 140, 20),
    #(850, screen.get_height() - 320, 180, 20),
#
    #(700, screen.get_height() - 400, 120, 15),
    #(500, screen.get_height() - 460, 100, 15),
    #(300, screen.get_height() - 520, 100, 15),
#
    #(200, screen.get_height() - 600, 300, 20),
]
platforms_group = pygame.sprite.Group()
for p_x, p_y, p_width, p_height in platforms_spec:
    platform = Platform(p_x, p_y, p_width, p_height, WHITE)
    platforms_group.add(platform)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # RENDER YOUR GAME HERE
    players_group.draw(screen)
    platforms_group.draw(screen)

    # When there will be more than one player
    for player in players_group:
        print(player)
        player.update(platforms_group)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
