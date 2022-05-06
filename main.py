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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 2, 0, 0, 1],
    [1, 0, 0, 2, 2, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1]
]

env = Map(map_val)

run = True
while run:

    window.blit(background, (0, 0))
    env.draw()
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
