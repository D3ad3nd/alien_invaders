import pygame

import const
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('E:/PyProjects/alien_invasion/sprites/player.png')
        self.rect = self.image.get_rect(midbottom=pos)
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

        self.laser_shot = pygame.sprite.Group()

        self.shot_sound = pygame.mixer.Sound('E:/PyProjects/alien_invasion/sound/shot.wav')
        self.shot_sound.set_volume(0.5)

    def player_control(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += const.PLAYER_SPEED
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= const.PLAYER_SPEED

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.shot_sound.play()

    def reload(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.laser_shot.add(Laser(self.rect.center, const.PLAYER_LASER_SPEED))

    def restrict_player(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= const.SCREEN_WEIGHT:
            self.rect.right = const.SCREEN_WEIGHT

    def update(self):
        self.player_control()
        self.restrict_player()
        self.reload()
        self.laser_shot.update()
