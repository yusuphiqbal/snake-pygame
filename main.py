from random import randint
import sys

import pygame
from pygame import Vector2


class Fruit:
    def __init__(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
    
    def draw(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (188, 71, 73), fruit_rect)


pygame.init()

cell_size = 40
cell_number = 20

screen  = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

fruit = Fruit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((167, 201, 87))
    fruit.draw()
    pygame.display.update()
    clock.tick(60)
