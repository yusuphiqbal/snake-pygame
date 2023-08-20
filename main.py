from random import randint
import sys

import pygame
from pygame import Vector2


class Snake:
    def __init__(self):
        pos = cell_number / 2
        self.body = [Vector2(pos -5, pos), Vector2(pos - 6, pos), Vector2(pos - 7, pos)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load('assets/images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('assets/images/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('assets/images/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('assets/images/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('assets/images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('assets/images/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('assets/images/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('assets/images/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('assets/images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('assets/images/body_horizontal.png').convert_alpha()

        self.body_bl = pygame.image.load('assets/images/body_bl.png').convert_alpha()
        self.body_br = pygame.image.load('assets/images/body_br.png').convert_alpha()
        self.body_tl = pygame.image.load('assets/images/body_tl.png').convert_alpha()
        self.body_tr = pygame.image.load('assets/images/body_tr.png').convert_alpha()
    
    def draw(self):
        self.update_head_graphics()

        for index, block in enumerate(self.body):
            rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, rect)
            else:
                pygame.draw.rect(screen, (56, 102, 65), rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

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
        rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, rect)

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
        self.check_fail()

    def draw(self):
        self.fruit.draw()
        self.snake.draw()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.spawn()
            self.snake.grow()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x or not self.snake.body[0].x < cell_number:
            self.over()

        if not self.snake.body[0].y >= 0 or not self.snake.body[0].y < cell_number:
            self.over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.over()

    @staticmethod
    def over():
        pygame.quit()
        sys.exit()


pygame.init()

cell_size = 40
cell_number = 20

screen  = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

apple = pygame.image.load('assets/images/apple.png').convert_alpha()

pygame.time.set_timer(pygame.USEREVENT, 150)

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.over()
        
        if event.type == pygame.USEREVENT:
            game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction.y != 1:
                game.snake.direction = Vector2(0, -1)
            
            if event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                game.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                game.snake.direction = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                game.snake.direction = Vector2(1, 0)


    screen.fill((167, 201, 87))
    game.draw()
    pygame.display.update()
    clock.tick(60)
