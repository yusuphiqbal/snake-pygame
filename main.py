from random import randint
import sys

import pygame
from pygame import Vector2


class Snake:
    def __init__(self):
        pos = cell_number / 2
        self.body = [Vector2(pos - 3, pos), Vector2(pos - 2, pos), Vector2(pos - 1, pos)]
        self.direction = Vector2(1, 0)
    
    def draw(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (56, 102, 65), block_rect)

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

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
snake = Snake()

pygame.time.set_timer(pygame.USEREVENT, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.USEREVENT:
            snake.move()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.direction = Vector2(0, -1)
            
            if event.key == pygame.K_DOWN:
                snake.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT:
                snake.direction = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT:
                snake.direction = Vector2(1, 0)


    screen.fill((167, 201, 87))
    fruit.draw()
    snake.draw()
    pygame.display.update()
    clock.tick(60)
