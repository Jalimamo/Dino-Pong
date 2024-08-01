import math
import random
import time

import pygame

from Settings import *


class Ball:

    def __init__(self, window, x, y, color, radius):
        self.window = window
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.x_vel, self.y_vel = self.define_starting_direction()
        self.border_time = -1
        self.has_bugged = False

    def draw(self):
        # TODO Ball (3) Draw the ball
        #  Which shape has a ball and how can we draw it?
        pygame.draw.circle(self.window, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, mpf):
        self.x += self.x_vel * mpf
        self.y += self.y_vel * mpf
        # TODO Ball (4) Move the ball
        #  How can we move the ball? Hint: We need a separate velocity in x and y direction.
        if self.y < BALL_UNSTUCK_BORDER or self.y > WIN_HEIGHT - BALL_UNSTUCK_BORDER:
            if self.border_time == -1:
                self.border_time = time.time()
            else:
                if time.time() - self.border_time > 1:
                    self.reset()
                    self.has_bugged = True
        else:
            self.border_time = -1


    def reset(self):
        self.x = WIN_WIDTH / 2
        self.y = WIN_HEIGHT / 2
        self.x_vel, self.y_vel = self.define_starting_direction()

    def define_starting_direction(self):
        # Defines a random starting direction of the ball.
        angle = 0
        while angle == 0:
            angle = math.radians(random.randrange(-30, 30))
        pos = -1 if random.random() > 0.5 else 1
        x_vel = pos * abs(math.cos(angle) * BALL_MAX_VEL)
        y_vel = math.sin(angle) * BALL_MAX_VEL
        return x_vel, y_vel

    # Used for powerups
    def change_speed(self, delta):
        if self.x_vel < 0:
            self.x_vel -= delta
        else:
            self.x_vel += delta

        if self.y_vel < 0:
            self.y_vel -= delta
        else:
            self.y_vel += delta
