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

        self.crunch_sound = pygame.mixer.Sound('assets/sounds/crunch.wav')
    
    def draw(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail, rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, rect)

                if previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, rect)

                if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                    screen.blit(self.body_tl, rect)
                
                if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                    screen.blit(self.body_bl, rect)

                if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                    screen.blit(self.body_tr, rect)

                if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                    screen.blit(self.body_br, rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

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

    def play_crunch_sound(self):
        self.crunch_sound.play()

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
        self.draw_grass()
        self.fruit.draw()
        self.snake.draw()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.play_crunch_sound()
            self.fruit.spawn()
            self.snake.grow()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.spawn()

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

    def draw_grass(self):
        grass_color = (118, 200, 147)

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score, True, (33, 33, 33))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

cell_size = 40
cell_number = 20

screen  = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

apple = pygame.image.load('assets/images/apple.png').convert_alpha()
game_font = pygame.font.Font('assets/fonts/PoetsenOne-Regular.ttf', 24)

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


    screen.fill((153, 217, 140))
    game.draw()
    pygame.display.update()
    clock.tick(60)
