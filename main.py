import pygame
import sys
import random

from player import Player
import laser
import const
import alien
import bg


class GameMech:
    def __init__(self):
        player_sprite = Player(const.PLAYER_START_POS)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives = 3
        self.live_surf = pygame.image.load('E:/PyProjects/alien_invasion/sprites/life.png')
        self.live_x_start_pos = const.SCREEN_WEIGHT - (self.live_surf.get_size()[0] * 2 + 20)

        self.score = 0
        self.score_font = pygame.font.Font('E:/PyProjects/alien_invasion/fonts/score_font.ttf', 20)

        self.aliens = pygame.sprite.Group()
        self.spawn_alien(rows=7, columns=7)
        self.alien_x_direction = 1
        self.alien_y_direction = 2
        self.alien_lasers_group = pygame.sprite.Group()

        music = pygame.mixer.Sound('E:/PyProjects/alien_invasion/sound/main.mp3')
        music.set_volume(0.3)
        music.play(loops=-1)

        self.hit_sound = pygame.mixer.Sound('E:/PyProjects/alien_invasion/sound/hit.wav')
        self.hit_sound.set_volume(0.5)

        self.shot_sound = pygame.mixer.Sound('E:/PyProjects/alien_invasion/sound/shot.wav')
        self.shot_sound.set_volume(0.5)

        self.win_music = pygame.mixer.Sound('E:/PyProjects/alien_invasion/sound/win.wav')
        self.win_music.set_volume(0.3)

    def run(self):
        # update sprites
        self.player.update()
        self.aliens.update(self.alien_x_direction)
        self.alien_lasers_group.update()
        # draw sprites
        self.player.sprite.laser_shot.draw(screen)
        self.player.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers_group.draw(screen)
        self.check_alien_position()
        self.collision_checker()
        self.display_lives()
        self.display_score()
        self.victory_message()

    def spawn_alien(self, rows, columns):
        for row_id, row in enumerate(range(rows)):
            for column_id, column in enumerate(range(columns)):
                x = const.ALIEN_X_DISTANCE * column_id + const.ALIEN_X_OFFSET
                y = const.ALIEN_Y_DISTANCE * row_id + const.ALIEN_Y_OFFSET

                if row_id == 0 or row_id == 1:
                    alien_sprite = alien.Alien('red_alien', x, y)
                elif row_id == rows - 1 or row_id == rows - 2:
                    alien_sprite = alien.Alien('green_alien', x, y)
                else:
                    alien_sprite = alien.Alien('blue_alien', x, y)
                self.aliens.add(alien_sprite)

    def check_alien_position(self):
        all_aliens = self.aliens.sprites()
        for i in all_aliens:
            if i.rect.left <= 0:
                self.alien_x_direction = 1
                self.move_alien_y()
            if i.rect.right >= const.SCREEN_WEIGHT:
                self.alien_x_direction = -1
                self.move_alien_y()

    def move_alien_y(self):
        for i in self.aliens:
            i.rect.y += self.alien_y_direction

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            alien_laser_sprite = laser.Laser(random_alien.rect.center, const.ALIEN_LASER_SPEED, )
            self.alien_lasers_group.add(alien_laser_sprite)
            self.shot_sound.play()

    def collision_checker(self):
        if self.player.sprite.laser_shot:
            for i in self.player.sprite.laser_shot:
                hit_alien = pygame.sprite.spritecollide(i, self.aliens, True)
                if hit_alien:
                    for elem in hit_alien:
                        self.score += elem.value
                    i.kill()
                    self.hit_sound.play()

        if self.alien_lasers_group:
            for i in self.alien_lasers_group:
                if pygame.sprite.spritecollide(i, self.player, False):
                    i.kill()
                    self.hit_sound.play()
                    self.lives -= 1
                    if self.lives == 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for i in self.aliens:
                if pygame.sprite.spritecollide(i, self.player, False):
                    print("Loser")

    def display_lives(self):
        for i in range(self.lives - 1):
            x = self.live_x_start_pos + (i * self.live_surf.get_size()[0])
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surface = self.score_font.render(f'score:{self.score}', False, (0, 204, 205))
        score_rect = score_surface.get_rect(topleft=(10, 10))
        screen.blit(score_surface, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.score_font.render('You Won', False, (0, 204, 205))
            victory_rect = victory_surf.get_rect(center=(const.SCREEN_WEIGHT / 2, const.SCREEN_HEIGHT / 2))
            screen.blit(victory_surf, victory_rect)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('E:/PyProjects/alien_invasion/sprites/bg.png')
        self.image = pygame.transform.scale(self.image, (const.SCREEN_WEIGHT, const.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0, 0)

    def display_bg(self):
        self.image.set_alpha(50)
        screen.blit(self.image, self.rect)


if __name__ == '__main__':
    pygame.init()
    game = GameMech()
    background = Background()

    screen = pygame.display.set_mode((const.SCREEN_WEIGHT, const.SCREEN_HEIGHT))
    pygame.display.set_caption("Aliens Invaders")

    ALIEN_SHOOT_EVENT = pygame.USEREVENT
    pygame.time.set_timer(ALIEN_SHOOT_EVENT, const.ALIEN_SHOOT_EVENT_TIME)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIEN_SHOOT_EVENT:
                game.alien_shoot()

        screen.fill(const.BG_COLOR)
        game.run()
        background.display_bg()

        pygame.display.flip()
        clock.tick(60)
