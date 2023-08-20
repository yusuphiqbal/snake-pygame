import sys

import pygame

pygame.init()

cell_size = 40
cell_number = 20

screen  = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((167, 201, 87))
    pygame.display.update()
    clock.tick(60)
