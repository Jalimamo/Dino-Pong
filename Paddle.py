import pygame
from Settings import *


class Paddle:
    def __init__(self, window, x, y, color):
        self.window = window
        self.x = x
        self.y = y
        self.color = color
        if self.color == (254, 254, 254):
            self.dino_image = pygame.image.load('img/Dino.png').convert_alpha()
            self.dino_rect = self.dino_image.get_rect()
        elif self.color == (253, 253, 253):
            self.bird_image = pygame.transform.scale_by(pygame.image.load('img/bird.png').convert_alpha(), BIRD_SCALE)
            self.bird_rect = self.bird_image.get_rect()


    def draw(self):
        # TODO Paddle (1) Draw the paddles
        #  Which shape has a paddle and how can we draw it?
        if self.color == (254, 254, 254):
            pygame.draw.rect(self.window, self.color, (self.x, self.y, self.dino_rect.width, self.dino_rect.height))
        elif self.color == (253, 253, 253):
            pygame.draw.rect(self.window, self.color, (self.x, self.y, self.bird_rect.width, self.bird_rect.height))
        else:
            pygame.draw.rect(self.window, self.color, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

    def move(self, upwards, mpf):
        if upwards:
            new_pos = self.y + (PADDLE_VEL * mpf)
            min_pos = 0
            if new_pos < min_pos:
                self.y = min_pos
            else:
                self.y -= PADDLE_VEL * mpf
        else:
            new_pos = self.y - (PADDLE_VEL * mpf)
            min_pos = WIN_HEIGHT - PADDLE_HEIGHT
            if new_pos > min_pos:
                self.y = min_pos
            else:
                self.y += PADDLE_VEL * mpf
