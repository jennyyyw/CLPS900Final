import sys

import pygame
from pygame.locals import *

pygame.init()

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Psycho Runner')

tile_dim = 50

background = pygame.image.load('background.png')

class Player():
    def __init__(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -8
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 1
        if key[pygame.K_RIGHT]:
            dx += 1


        #add gravity
        self.vel_y += 0.25
        if self.vel_y > 1:
            self.vel_y = 1
        dy += self.vel_y

        #check for collision
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

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0

        #draw player onto screen
        window.blit(self.image, self.rect)
        pygame.draw.rect(window, (255, 255, 255), self.rect, 2)


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
                col_val += 1
            row_val += 1

    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])


map_val = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 2, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, height - 130)
env = Map(map_val)

run = True
while run:

    window.blit(background, (0, 0))
    env.draw()
    player.update()
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
