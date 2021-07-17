import random
import pyganim
import pygame

from settings import WIDTH, HEIGHT


class Plasmoid(pygame.sprite.Sprite):
    speed = -15

    def __init__(self, position):
        super(Plasmoid, self).__init__()

        self.image = pygame.image.load('images/plasmoid/plasmoid.png')
        self.image = pygame.transform.scale(self.image, (40, 25))

        self.rect = self.image.get_rect()

        self.rect.midbottom = position

    def update(self):
        self.rect.move_ip(0, self.speed)


class Player(pygame.sprite.Sprite):
    max_speed = 10
    shooting_cooldown = 150

    def __init__(self, clock, plasmoids):
        super(Player, self).__init__()

        self.clock = clock
        self.plasmoids = plasmoids

        self.image = pygame.image.load('images/persons/player/character_maleAdventurer_attack0.png')
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT

        self.current_speed = 0

        self.current_shooting_cooldown = 0

        self.plasmoids_sound = pygame.mixer.Sound('sounds/vyiigryish.wav')


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.current_speed = - self.max_speed
        elif keys[pygame.K_RIGHT]:
            self.current_speed = self.max_speed
        else:
            self.current_speed = 0

        self.rect.move_ip((self.current_speed, 0))

        self.process_shooting()

    def process_shooting(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.current_shooting_cooldown <= 0:
            self.plasmoids.add(Plasmoid(self.rect.midtop))
            self.current_shooting_cooldown = self.shooting_cooldown
            self.plasmoids_sound.play()
        else:
            self.current_shooting_cooldown -= self.clock.get_time()

        for plasmoid in list(self.plasmoids):
            if plasmoid.rect.bottom < 0:
                self.plasmoids.remove(plasmoid)


class Background(pygame.sprite.Sprite):

    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load('images/backgrounds/backgrond.jpg')
        self.rect = self.image.get_rect()

        self.rect.bottom = HEIGHT

    def update(self):
        self.rect.bottom += 5

        if self.rect.bottom >= self.rect.height:
            self.rect.bottom = HEIGHT


class Meteorit(pygame.sprite.Sprite):
    cooldown = 250
    current_cooldown = 0
    speed = 10

    def __init__(self):
        super(Meteorit, self).__init__()

        image_name = 'images/meteorits/meteor{}.png'.format(random.randint(1, 10))
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (random.randint(0, WIDTH), 0)

    def update(self):
        self.rect.move_ip((0, self.speed))

    @staticmethod
    def process_meteors(clock, meteorites):
        if Meteorit.current_cooldown <= 0:
            meteorites.add(Meteorit())
            Meteorit.current_cooldown = Meteorit.cooldown
        else:
            Meteorit.current_cooldown -= clock.get_time()

        for m in list(meteorites):
            if (m.rect.right < 0 or
                    m.rect.left > WIDTH or
                    m.rect.top > HEIGHT):
                meteorites.remove(m)
