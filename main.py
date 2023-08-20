from random import randint
import sys

import pygame
from pygame import Vector2


class Snake:
    def __init__(self):
        pos = cell_number / 2
        self.body = [Vector2(pos - 3, pos), Vector2(pos - 2, pos), Vector2(pos - 1, pos)]
        self.direction = Vector2(1, 0)
        self.new_block = False
    
    def draw(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (56, 102, 65), block_rect)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def grow(self):
        self.new_block = True

class Fruit:
    def __init__(self):
        self.spawn()
    
    def draw(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (188, 71, 73), fruit_rect)

    def spawn(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Game:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
    
    def update(self):
        self.snake.move()
        self.check_collision()

    def draw(self):
        self.fruit.draw()
        self.snake.draw()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.spawn()
            self.snake.grow()

pygame.init()

cell_size = 40
cell_number = 20

screen  = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

pygame.time.set_timer(pygame.USEREVENT, 150)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.USEREVENT:
            game.update()


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.snake.direction = Vector2(0, -1)
            
            if event.key == pygame.K_DOWN:
                game.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT:
                game.snake.direction = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT:
                game.snake.direction = Vector2(1, 0)


    screen.fill((167, 201, 87))
    game.draw()
    pygame.display.update()
    clock.tick(60)
