import datetime
import os

import pygame

pygame.init()

# Game Settings
WIN_WIDTH, WIN_HEIGHT = 1500, 1000
FPS = 60
SPEED_MULTIPLIER = 70
FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 3

# Color converter: https://www.rapidtables.com/convert/color/rgb-to-hex.html
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# Decide if you want to use a background image.
# BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "Tennis.png")), (WIN_WIDTH, WIN_HEIGHT))
BG_IMG = None

# Paddle Settings
PADDLE_VEL = 7
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

# Ball Settings
BALL_MAX_VEL = 7
BALL_RADIUS = 7
BALL_UNSTUCK_BORDER = 10

# Powerup Settings
POWERUPS_ENABLED = True
POWERUP_SIZE = BALL_RADIUS * 7
POWERUP_SPAWN_DELAY = 10
POWERUP_DISPLAY_TIME = 15
POWERUP_DURATION = 10_000
# POWERUP_BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "Powerup.png")), (POWERUP_SIZE, POWERUP_SIZE))
POWERUP_BG_IMG = None
ENABLED_POWERUPS = [
    # Add custom powerups to this list
    "FastBall",
    "FastPaddle",
]


DINO1 = True
DINO2 = True
BIRD = True
ANIMAL_COLLISION = True

BIRD_SCALE = 4
PIPE_SCALE = 1
PIPE_COUNT = 3
GAP_SIZE = 250
