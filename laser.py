import pygame
import const


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, laser_speed):
        super().__init__()
        self.image = pygame.image.load('E:/PyProjects/alien_invasion/sprites/laser.png')
        self.rect = self.image.get_rect(center=pos)
        self.laser_speed = laser_speed

    def destroy_laser(self):
        if self.rect.y <= -50 or self.rect.y >= const.SCREEN_HEIGHT + 10:
            self.kill()

    def update(self):
        self.rect.y += self.laser_speed
        self.destroy_laser()
