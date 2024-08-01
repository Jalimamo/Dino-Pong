import pygame
import random
from Settings import *

# Initialisierung von Pygame
pygame.init()

# Bildschirmabmessungen
WIDTH, HEIGHT = 600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Farben
WHITE = (255, 255, 255)

# Vogel-Klasse
class Bird:
    def __init__(self):
        self.image = pygame.transform.scale_by(pygame.image.load('img/bird.png').convert_alpha(), BIRD_SCALE)
        self.rect = self.image.get_rect(center=(WIN_WIDTH - self.image.get_rect().width / 2, WIN_HEIGHT - self.image.get_rect().height / 2))
        self.rect.x = (WIN_WIDTH - self.rect.width) // 2
        self.rect.y = (WIN_HEIGHT - self.rect.height) // 2
        self.jump_speed = -10
        self.gravity = 0.5
        self.velocity = 0

    def jump(self):
        self.velocity = self.jump_speed

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Hindernis-Klasse
class Pipe:
    def __init__(self, x, gap_size=200):
        self.image = pygame.transform.scale_by(pygame.image.load('img/pipe.png').convert_alpha(), PIPE_SCALE)
        self.stem_image = pygame.transform.scale_by(pygame.image.load('img/pipe_stem.png').convert_alpha(), PIPE_SCALE)
        self.gap_size = gap_size
        self.rect_top = self.image.get_rect()
        self.rect_bottom = self.image.get_rect()
        self.rect_top.x = self.rect_bottom.x = x
        self.set_height()

    def set_height(self):
        height = random.randint(50, HEIGHT - self.gap_size - 50)
        self.rect_top.y = 0
        self.rect_top.height = height
        self.rect_bottom.y = height + self.gap_size
        self.rect_bottom.height = WIN_HEIGHT - self.rect_bottom.y

    def update(self):
        self.rect_top.x -= 5
        self.rect_bottom.x -= 5
        if self.rect_top.x < -self.rect_top.width:
            self.rect_top.x = self.rect_bottom.x = WIN_WIDTH
            self.set_height()

    def draw(self, screen):
        pipe_height = pygame.image.load('img/pipe.png').get_height() * PIPE_SCALE
        screen.blit(pygame.transform.flip(self.image, False, True), (self.rect_top.left, self.rect_top.bottom - pipe_height))
        for i in range(0, int(self.rect_top.bottom - pipe_height), self.stem_image.get_height()):
            screen.blit(self.stem_image, (self.rect_top.x, i))

        screen.blit(self.image, self.rect_bottom.topleft)
        for i in range(self.rect_bottom.y + self.image.get_height(), WIN_HEIGHT, self.stem_image.get_height()):
            screen.blit(self.stem_image, (self.rect_bottom.x, i))

# Hauptspielklasse


class Bird_Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        pipe_width = pygame.image.load('img/pipe.png').get_width() * PIPE_SCALE
        self.pipes = [Pipe(WIN_WIDTH + i * ((WIN_WIDTH + pipe_width) / PIPE_COUNT)) for i in range(PIPE_COUNT)]
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.game_over = False

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.bird.jump()
                if event.key == pygame.K_b and self.game_over:
                    self.__init__(self.screen)  # Neustart des Spiels

        if not self.game_over:
            self.bird.update()
            for pipe in self.pipes:
                pipe.update()
                if self.bird.rect.colliderect(pipe.rect_top) or self.bird.rect.colliderect(pipe.rect_bottom):
                    self.game_over = True
            if self.bird.rect.top <= 0 or self.bird.rect.bottom >= WIN_HEIGHT:
                self.game_over = True

            # Score update
            for pipe in self.pipes:
                if pipe.rect_top.right < self.bird.rect.left < pipe.rect_top.right + 5:
                    self.score += 1


    def draw(self):
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
            # pygame.draw.rect(self.screen, WHITE, pipe.rect_top)
            # pygame.draw.rect(self.screen, WHITE, pipe.rect_bottom)

        # Punktestand anzeigen
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (WIDTH // 4, (HEIGHT // 2 ) + 30))

        if self.game_over:
            game_over_text = self.font.render('Game Over! Press B to Restart', True, WHITE)
            self.screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))

if __name__ == "__main__":
    game = Bird_Game(screen)
    while True:
        game.run()
        game.draw()