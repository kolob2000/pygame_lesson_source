import sys
import pygame
import pyganim
from settings import SIZE, WHITE
from game_objects import Player, Background, Plasmoid, Meteorit

pygame.init()
pygame.display.set_caption('Hello world')

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

explosion_animation = pyganim.PygAnimation([
    (f'images/explosion/explosion{i}.png', 50) for i in range(1, 9)
], loop=False)

music = pygame.mixer.Sound('sounds/Sound_07024.wav')
music.play(-1)

# Groups
all_objects = pygame.sprite.Group()
plasmoids = pygame.sprite.Group()
meteors = pygame.sprite.Group()

explosions = []
# Game objects
player = Player(clock, plasmoids)
background = Background()

all_objects.add(background)
all_objects.add(player)

# all_objects.add(Meteorit())
# all_objects.add(Plasmoid(player.rect.midtop))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    screen.fill(WHITE)
    # player.update()
    # background.update()
    # screen.blit(background.image, background.rect)
    # screen.blit(player.image, player.rect)
    Meteorit.process_meteors(clock, meteors)

    all_objects.update()
    plasmoids.update()
    meteors.update()

    meteors_and_plasmoids_collided = pygame.sprite.groupcollide(meteors, plasmoids, True, True)

    for collided in meteors_and_plasmoids_collided:
        explosion = explosion_animation.getCopy()
        explosion.play()
        explosions.append((explosion, (collided.rect.center)))

    player_and_meteors_collided = pygame.sprite.spritecollide(player, meteors, True)

    if player_and_meteors_collided:
        all_objects.remove(player)

    all_objects.draw(screen)
    plasmoids.draw(screen)
    meteors.draw(screen)

    for explosion, position in explosions.copy():
        if explosion.isFinished():
            explosions.remove((explosion, position))
        else:
            x, y = position
            explosion.blit(screen, (x - 128, y - 128))

    pygame.display.flip()
    clock.tick(30)
# 1:07
