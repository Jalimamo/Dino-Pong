import pygame
import random
from Settings import *

# Initialisierung von Pygame
pygame.init()

# Farben
BLACK = (0, 0, 0)
GROUND = WIN_HEIGHT - 30  # HEIGHT - 50, assuming HEIGHT is 400
INVERTED_GROUND = 30

# Dino-Klasse
class Dino:
    def __init__(self, inverted):
        self.inverted = inverted
        self.image = pygame.image.load('img/Dino.png').convert_alpha()
        if inverted:
            self.image = pygame.transform.flip(self.image, True, True)
        self.rect = self.image.get_rect()
        if inverted:
            print()
            self.rect.x = WIN_WIDTH - 50 - self.rect.width
            self.rect.y = INVERTED_GROUND
            self.jump_speed = - 10
            self.gravity = -4
        else:
            self.rect.x = 50
            self.rect.y = GROUND - self.rect.height
            self.jump_speed = 10
            self.gravity = 4
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            if self.inverted:
                self.jump_speed = 60
            else:
                self.jump_speed = -60

    def update(self, mpf):
        if self.is_jumping:
            self.jump_speed += self.gravity * mpf
            self.rect.y += self.jump_speed * mpf
            if self.inverted:
                if self.rect.y <= INVERTED_GROUND:
                    self.rect.y = INVERTED_GROUND
                    self.is_jumping = False
            else:
                if self.rect.y >= GROUND - self.rect.height:
                    self.rect.y = GROUND - self.rect.height
                    self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Hindernis-Klasse
class Obstacle:
    def __init__(self, speed, inverted):
        self.inverted = inverted
        self.image = pygame.image.load('img/Cactus.png').convert_alpha()
        if inverted:
            self.image = pygame.transform.flip(self.image, True, True)
        scale_factor = random.uniform(0.5, 1.5)  # Zufällige Größe des Kaktus
        self.startwidth = self.image.get_width()
        self.startheight = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(self.startwidth * scale_factor), int(self.startheight * scale_factor)))
        self.rect = self.image.get_rect()
        if self.inverted:
            self.rect.x = 0  # WIDTH, assuming WIDTH is 800
            self.rect.y = INVERTED_GROUND
            self.speed = speed * -1
        else:
            self.rect.x = WIN_WIDTH  # WIDTH, assuming WIDTH is 800
            self.rect.y = GROUND - self.rect.height
            self.speed = speed


    def randomize_size(self):
        self.image = pygame.image.load('img/Cactus.png').convert_alpha()
        if self.inverted:
            self.image = pygame.transform.flip(self.image, True, True)
        scale_factor = random.uniform(0.5, 1.5)  # Zufällige Größe des Kaktus
        self.image = pygame.transform.scale(self.image, (int(self.startwidth * scale_factor), int(self.startheight * scale_factor)))
        self.rect = self.image.get_rect()
        if self.inverted:
            self.rect.y = INVERTED_GROUND
        else:
            self.rect.y = GROUND - self.rect.height

    def update(self, mpf):
        self.rect.x -= self.speed * mpf
        if self.inverted:
            if self.rect.x > WIN_WIDTH:
                self.randomize_size()
                self.rect.x = 0 - random.randint(100, 300)  # WIDTH
                self.speed -= 0.5  # Hindernis wird schneller
        else:
            if self.rect.x < -self.rect.width:
                self.randomize_size()
                self.rect.x = WIN_WIDTH + random.randint(100, 300)  # WIDTH
                self.speed += 0.5  # Hindernis wird schneller




    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Hauptspielklasse
class Dino_Game:
    def __init__(self, screen,inverted):
        self.inverted = inverted
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dino = Dino(inverted)
        self.obstacles = [Obstacle(speed=15, inverted=inverted)]
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.game_over = False

    def run(self, mpf):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.dino.jump()
                if event.key == pygame.K_r and self.game_over:
                    self.__init__(self.screen)  # Neustart des Spiels

        if not self.game_over:
            self.dino.update(mpf)
            for obstacle in self.obstacles:
                obstacle.update(mpf)
                if self.dino.rect.colliderect(obstacle.rect):
                    self.game_over = True

            self.score += 1

    def draw(self):
        self.dino.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Punktestand anzeigen
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        if self.inverted:
            self.screen.blit(score_text, (10, 10))
        else:
            self.screen.blit(score_text, (WIN_WIDTH -150, WIN_HEIGHT - 30))

        if self.game_over:
            if self.inverted:
                game_over_text = self.font.render('Game Over! Press Plus to Restart', True, (255, 255, 255))
                self.screen.blit(game_over_text, (WIN_WIDTH // 4, WIN_HEIGHT // 4))  # WIDTH // 4, HEIGHT // 2
            else:
                game_over_text = self.font.render('Game Over! Press Right Click to Restart', True, (255, 255, 255))
                self.screen.blit(game_over_text, (WIN_WIDTH // 4,(WIN_HEIGHT // 4) * 3)) # WIDTH // 4, HEIGHT // 2

        #pygame.display.flip()
        #self.clock.tick(30)

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 400))  # WIDTH, HEIGHT
    game = Dino_Game(screen)
    while True:
        game.run()
