import random
from random import randrange

import pygame

from Settings import GREEN, POWERUP_SIZE, WIN_HEIGHT, WIN_WIDTH, PADDLE_VEL, WHITE, YELLOW, BLUE, MAGENTA, \
    POWERUP_BG_IMG, RED, ENABLED_POWERUPS


class Powerups:
    def __init__(self):
        self.x, self.y = get_random_position()
        self.current_powerup = None

    def draw(self, win):
        if POWERUP_BG_IMG is None:
            self.draw_mario_kart_mystery_box(win)
        else:
            win.blit(POWERUP_BG_IMG, (self.x, self.y))

    def draw_mario_kart_mystery_box(self, win):
        square_size = POWERUP_SIZE // 4
        colors = [MAGENTA, BLUE, GREEN, YELLOW]

        for row in range(4):
            color = colors[row]
            for col in range(4):
                if (row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0):
                    coordinates = (self.x + col * square_size, self.y + row * square_size, square_size, square_size)
                    pygame.draw.rect(win, color, coordinates)

        points = [(self.x, self.y),
                  (self.x + POWERUP_SIZE, self.y),
                  (self.x + POWERUP_SIZE, self.y + POWERUP_SIZE),
                  (self.x, self.y + POWERUP_SIZE)]
        pygame.draw.lines(win, WHITE, True, points, 3)

    def activate(self, game):
        self.current_powerup = get_random_powerup()
        self.current_powerup.activate(game)

    def deactivate(self, game):
        self.current_powerup.deactivate(game)
        self.current_powerup = None


# Convention: Every powerup class must have:
#   - name attribute
#   - activate(self, game) method
#   - deactivate(self, game) method

class FastBall:
    def __init__(self):
        self.name = "Fast Ball"
        self.ball_speedup = 5

    def activate(self, game):
        game.ball.change_speed(self.ball_speedup)
        # TODO: make game.ball faster

    def deactivate(self, game):
        game.ball.change_speed(-self.ball_speedup)
        # TODO: restore the original speed of game.ball
        pass


class FastPaddle:
    def __init__(self):
        self.name = "Fast Paddle"
        self.paddle = None

    def activate(self, game):
        # TODO: set self.paddle to either game.left_paddle or game.right_paddle depending on which player
        #  hit the powerup. Use an if-else construct.

        self.paddle.vel = PADDLE_VEL * 1.5

    def deactivate(self, game):
        # TODO: restore original paddle speed
        self.paddle = None
        pass


def get_random_powerup():
    powerups = []

    for powerup in ENABLED_POWERUPS:
        # Add case distinctions for custom powerups
        if True: #powerup == "FastBall":
            powerups.append(FastBall())
        elif powerup == "FastPaddle":
            powerups.append(FastPaddle())

    return random.choice(powerups)


def get_random_position() -> (int, int):
    x = randrange(0, WIN_WIDTH - POWERUP_SIZE)
    y = randrange(0, WIN_HEIGHT - POWERUP_SIZE)
    return x, y
