import random
import time

import pygame

import Powerups
import dino
import BirdGame
from Paddle import Paddle
from Ball import Ball
from Settings import *
from Powerups import Powerups

#pygame.init()


class Game:

    def __init__(self, window):
        self.window = window
        self.left_paddle = Paddle(window, 5, (WIN_HEIGHT - PADDLE_HEIGHT) / 2 , RED)
        self.right_paddle = Paddle(window, WIN_WIDTH - (PADDLE_WIDTH + 5), (WIN_HEIGHT - PADDLE_HEIGHT) / 2, BLUE)
        self.ball = Ball(window, WIN_WIDTH / 2, WIN_HEIGHT / 2, GREEN, BALL_RADIUS)
        self.left_score = 0
        self.right_score = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
        if DINO1:
            self.dino_game = dino.Dino_Game(window, False)
            self.dino_paddle = Paddle(window, self.dino_game.dino.rect.x, self.dino_game.dino.rect.y, (254, 254, 254))
        if DINO2:
            self.inverted_dino_game = dino.Dino_Game(window, True)
            self.idino_paddle = Paddle(window, self.inverted_dino_game.dino.rect.x, self.inverted_dino_game.dino.rect.y, (254, 254, 254))
        if BIRD:
            self.bird_game = BirdGame.Bird_Game(window)
            self.bird_paddle = Paddle(window, self.bird_game.bird.rect.x, self.bird_game.bird.rect.y, (253, 253, 253))

        if ENABLED_POWERUPS:
            self.powerups = Powerups()
            self.powerups_active = False
            self.powerups_visible = False
            self.last_powerup_time = time.time()

    def draw(self):
        # This is our central draw method. If we want to display something on the screen, we have to add it in here.
        self.frame_count += 1
        if time.time() - self.start_time > 1:
            self.start_time = time.time()
            self.fps = self.frame_count
            self.frame_count = 0
        # Define the background.
        if BG_IMG is None:
            # Fill the background with a specified color.
            self.window.fill(BLACK)
        else:
            # Fill the background with an image you can specify in the Settings.py file.
            self.window.blit(BG_IMG, (0, 0))
        if DINO1:
            self.dino_game.draw()
        if DINO2:
            self.inverted_dino_game.draw()
            # Draw the dividing lines in the middle
        self.draw_divider()

        if POWERUPS_ENABLED and self.powerups_visible:
            if time.time() - self.last_powerup_time > POWERUP_DISPLAY_TIME:
                self.powerups.draw()

        # TODO Paddle (1) Draw the paddles
        self.left_paddle.draw()
        self.right_paddle.draw()

        if DINO1:
            self.dino_paddle.x = self.dino_game.dino.rect.x
            self.dino_paddle.y = self.dino_game.dino.rect.y
            #self.dino_paddle.draw()
        if DINO2:
            self.idino_paddle.x = self.inverted_dino_game.dino.rect.x
            self.idino_paddle.y = self.inverted_dino_game.dino.rect.y
        if BIRD:
            self.bird_paddle.x = self.bird_game.bird.rect.x
            self.bird_paddle.y = self.bird_game.bird.rect.y
            # self.bird_paddle.draw()

        # TODO Ball (3) Draw the ball
        self.ball.draw()

        # TODO Score (7) Draw the score
        self.draw_text(str(self.left_score), 20, 60)
        self.draw_text(str(self.right_score), WIN_WIDTH - 60, WIN_HEIGHT - 90)
        self.draw_text(f"FPS:{self.fps}", WIN_WIDTH / 2, WIN_HEIGHT / 2, RED)


        if BIRD:
            self.bird_game.draw()

        # We have to call this one to make sure our drawings get displayed.
        pygame.display.update()

    def draw_divider(self):
        # Draws the dividing lines in the middle of the screen.
        for i in range(10, WIN_HEIGHT, WIN_HEIGHT // 5):
            pygame.draw.rect(self.window, WHITE, (WIN_WIDTH // 2 - 5, i, 10, WIN_HEIGHT // 15))

    def draw_text(self, text, x, y, color=WHITE) -> None:
        text = FONT.render(text, True, color)
        x = x - text.get_width() // 2
        self.window.blit(text, (x, y))

    # TODO Paddle (2) Move the paddles
    #   They should respond to key presses.
    def move_paddle_keys(self, keys, left, right, mpf):
        # TODO: define "up" and "down" keys for left and right paddle
        left_paddle_up_key = pygame.K_w
        left_paddle_down_key = pygame.K_s
        right_paddle_up_key = pygame.K_UP
        right_paddle_down_key = pygame.K_DOWN
        if DINO2:
            idino_jump = pygame.K_KP_ENTER
            idino_reset = pygame.K_KP_PLUS
        if BIRD:
            bird_jump = pygame.K_SPACE
            bird_reset = pygame.K_b

        # Move left paddle upwards with w and downwards with s
        if keys[left_paddle_up_key] and left:
            upwards = True  # TODO: True or False?
            self.left_paddle.move(upwards, mpf)
        if keys[left_paddle_down_key] and left:
            upwards = False  # TODO: True or False?
            self.left_paddle.move(upwards, mpf)

        # Move right paddle upwards with up arrow and downwards with down arrow
        if keys[right_paddle_up_key] and right:
            upwards = True  # TODO: True or False?
            self.right_paddle.move(upwards, mpf)
        if keys[right_paddle_down_key] and right:
            upwards = False  # TODO: True or False?
            self.right_paddle.move(upwards, mpf)

        if DINO1:
            if pygame.mouse.get_pressed()[0]:
                self.dino_game.dino.jump()
            if pygame.mouse.get_pressed()[2]:
                self.dino_game.__init__(self.window, False)
        if DINO2:
            if keys[idino_jump]:
                self.inverted_dino_game.dino.jump()
            if keys[idino_reset]:
                self.inverted_dino_game.__init__(self.window, True)
        if BIRD:
            if keys[bird_jump]:
                self.bird_game.bird.jump()
            if keys[bird_reset]:
                self.bird_game.__init__(self.window)

        if DINO1:
            self.dino_game.run(mpf)
        if DINO2:
            self.inverted_dino_game.run(mpf)
        if BIRD:
            self.bird_game.run(mpf)

    # region TODO (6) Collision detection
    # TODO Ball (6) Collision detection
    def handle_collision(self):
        if POWERUPS_ENABLED and self.powerups_visible and self.ball_hits_powerup():
            self.handle_powerup_collision()
        if self.ball_hits_ceiling_or_floor():
            self.ball.y_vel *= -1

        if self.ball_hits_paddle(self.left_paddle):
            self.handle_paddle_collision(self.left_paddle)

        elif self.ball_hits_paddle(self.right_paddle):
            self.handle_paddle_collision(self.right_paddle)

        if DINO1:
            if self.ball_hits_paddle(self.dino_paddle):
                self.handle_paddle_collision(self.dino_paddle)
        if DINO2:
            if self.ball_hits_paddle(self.idino_paddle):
                self.handle_paddle_collision(self.idino_paddle)
        if BIRD:
            if self.ball_hits_paddle(self.bird_paddle):
                self.handle_paddle_collision(self.bird_paddle)

    def ball_hits_ceiling_or_floor(self):
        # TODO: condition must be True when ball hits the ceiling or bottom, False otherwise
        if self.ball.y < 0 or self.ball.y > WIN_HEIGHT:
            return True
        return False

    def ball_hits_paddle(self, paddle):
        # TODO: condition must be True when ball hits the paddle, False otherwise
        if DINO1:
            if paddle == self.dino_paddle:
                if pygame.Rect(paddle.x, paddle.y, paddle.dino_rect.width, paddle.dino_rect.height).collidepoint(self.ball.x, self.ball.y) and ANIMAL_COLLISION:
                    return True
                    pass
                return False
        if DINO2:
            if paddle == self.idino_paddle:
                if pygame.Rect(paddle.x, paddle.y, paddle.dino_rect.width, paddle.dino_rect.height).collidepoint(self.ball.x, self.ball.y) and ANIMAL_COLLISION:
                    return True
                    pass
                return False
        if BIRD:
            if paddle == self.bird_paddle:
                if pygame.Rect(paddle.x, paddle.y, paddle.bird_rect.width, paddle.bird_rect.height).collidepoint(self.ball.x, self.ball.y) and ANIMAL_COLLISION:
                    return True
                    pass
                return False

        if pygame.Rect(paddle.x, paddle.y, PADDLE_WIDTH, PADDLE_HEIGHT).collidepoint(self.ball.x, self.ball.y):
            return True
        return False

    def ball_hits_powerup(self):
        return pygame.Rect(self.powerups.x, self.powerups.y, POWERUP_SIZE, POWERUP_SIZE).collidepoint(self.ball.x, self.ball.y)

    def handle_powerup_collision(self):
        self.powerups.activate(self)
        self.powerups_active = True
        self.hide_powerups()

    def handle_paddle_collision(self, paddle):
        # Reverse direction
        self.ball.x_vel *= - 1

        # Change y_vel based on where we hit the paddle
        middle_y = paddle.y + PADDLE_HEIGHT / 2
        difference_y = middle_y - self.ball.y
        reduction_factor = (PADDLE_HEIGHT / 2) / BALL_MAX_VEL
        y_vel = difference_y / reduction_factor
        y_vel = BALL_MAX_VEL if abs(y_vel) > BALL_MAX_VEL else y_vel
        y_vel += random.uniform(-1, 1)  # Avoid endless loops without having to move the paddle
        self.ball.y_vel = -1 * y_vel

    # endregion

    # region TODO (7) Draw the score
    # TODO Score (7) Draw the score
    def draw_score(self):
        # TODO: replace -1 with the correct computations
        one_fourth_window_width = -1
        three_fourths_window_width = -1

        self.draw_text(str(self.left_score), one_fourth_window_width, 20)
        self.draw_text(str(self.right_score), three_fourths_window_width, WIN_HEIGHT - 20)

    # endregion

    # region TODO (8) Winning condition
    # TODO Winning condition (8) Draw winning condition
    def draw_winning_text(self, player_name):
        self.draw()
        self.draw_text(player_name + " Player Won", WIN_WIDTH // 2, WIN_HEIGHT // 2 - 90)
        pygame.display.update()
        pygame.time.delay(5000)

    # TODO Winning condition (8) Check if one player has won the game
    def check_winning_condition(self):
        # TODO: replace False with the correct conditions
        left_player_won = False
        right_player_won = False

        # TODO: draw winning text depending on which player won
        if left_player_won:
            return True
        elif right_player_won:
            return True
        else:
            return False

    # endregion

    # region TODO (B) Output handling
    def move_paddle_networks(self, is_left, network_output):
        if network_output == 0:
            pass

        # 1 means we move upwards
        elif network_output == 1:
            if is_left:
                self.left_paddle.move(True)
            else:
                self.right_paddle.move(True)
                # What to do?

        # 2 means we move downwards
        else:
            if is_left:
                self.left_paddle.move(False)
            else:
                self.right_paddle.move(False)

    # endregion
    def hide_powerups(self):
        self.powerups_visible = False
        self.last_powerup_time = time.time()

    def spawn_powerup(self):
        self.powerups_active = False
        self.powerups_visible = True
        self.last_powerup_time = time.time()

