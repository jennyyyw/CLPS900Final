import sys

import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Psycho Runner')

game_over = 0
tile_dim = 50

font = pygame.font.Font(None, 32)

end_text = font.render('GAME OVER', True, (235, 0, 0), 0)

end_rect = end_text.get_rect()

end_rect.center = (width // 2, height // 3)

background = pygame.image.load('background.png')


class Player():
    def __init__(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (30, 50))
        self.dead_img = pygame.image.load('dead.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self, game):
        dx = 0
        dy = 0

        # get keypresses
        if game == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.jumped == False:
                self.vel_y = -8
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 1
            if key[pygame.K_RIGHT]:
                dx += 1

            # add gravity
            self.vel_y += 0.25
            if self.vel_y > 1:
                self.vel_y = 1
            dy += self.vel_y

            # check for collision
            for tile in env.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > height:
                self.rect.bottom = height
                dy = 0

            # check for collision with obstacles
            if pygame.sprite.spritecollide(self, obstacle_group, False):
                game = -1



        elif game == -1:
            self.image = self.dead_img
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player onto screen
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, (255,255,255), self.rect, 2)

        return game

def make_grid():
    for line in range(0, 10):
        pygame.draw.line(window, (255, 255, 255), (0, line * tile_dim), (width, line * tile_dim))
        pygame.draw.line(window, (255, 255, 255), (line * tile_dim, 0), (line * tile_dim, height))


class Map():
    def __init__(self, data):
        self.tile_list = []

        dirt_img = pygame.image.load('dirt.png')
        sand_img = pygame.image.load('sand.png')

        row_val = 0
        for row in data:
            col_val = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_dim, tile_dim))
                    img_rect = img.get_rect()
                    img_rect.x = col_val * tile_dim
                    img_rect.y = row_val * tile_dim
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(sand_img, (tile_dim, tile_dim))
                    img_rect = img.get_rect()
                    img_rect.x = col_val * tile_dim
                    img_rect.y = row_val * tile_dim
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    obstacle = Obstacle(col_val * tile_dim, row_val * tile_dim + 15)
                    obstacle_group.add(obstacle)
                col_val += 1
            row_val += 1

    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('obstacle.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 0.25
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -0.25
        pygame.draw.rect(window, (255, 255, 255), self.rect)


map_val = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 0, 2, 2, 0, 0, 0],
    [0, 2, 1, 1, 2, 1, 1, 2, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, height - 130)

obstacle_group = pygame.sprite.Group()

env = Map(map_val)

run = True
while run:

    window.blit(background, (0, 0))
    env.draw()
    if game_over == 0:
        obstacle_group.update()
    obstacle_group.draw(window)
    game_over = player.update(game_over)
    if game_over == -1:
        window.blit(end_text, end_rect)
    make_grid()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
