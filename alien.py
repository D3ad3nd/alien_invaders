import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_type, alien_x, alien_y):
        super().__init__()
        alien_path = 'E:/PyProjects/alien_invasion/sprites/' + alien_type + '.png'
        self.image = pygame.image.load(alien_path)
        self.rect = self.image.get_rect(topleft=(alien_x, alien_y))

        if alien_type == 'green_alien':
            self.value = 20
        elif alien_type == 'blue_alien':
            self.value = 50
        else:
            self.value = 100

    def update(self, alien_direction):
        self.rect.x += alien_direction
