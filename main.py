import pygame
from pygame.locals import *

pygame.init()

width = 900
height = 900

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Psycho Runner')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
