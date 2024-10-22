from Game import Game
from Settings import *
import time

if __name__ == "__main__":
    # Set the window width and height and initialise the game.
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("2-Player Mode")
    game = Game(window)

    # Game loop which gets repeated all the time.
    run = True
    clock = pygame.time.Clock()  # The clock helps us to limit the upper frame rate.
    while run:
        ms_frame = clock.tick(FPS)
        mpf = SPEED_MULTIPLIER * ms_frame / 1000 #mpf = move per frame
        game.draw()

        # This for loop is responsible for closing the window if we click on the red close button.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # TODO Paddle (2) Move the paddles
        #  Sense the currently pressed key and move the paddle up or down.
        keys = pygame.key.get_pressed()
        game.move_paddle_keys(keys, True, True, mpf)

        # TODO Ball (4) Move the ball
        game.ball.move(mpf)

        # TODO Ball (6) Collision detection
        game.handle_collision()

        # TODO Ball (5) Reset the ball
        if game.ball.x < 0:
            game.ball.reset()
            game.right_score += 1
        elif game.ball.x >= WIN_WIDTH:
            game.ball.reset()
            game.left_score += 1

        if POWERUPS_ENABLED:
            if game.powerups_active:
                if time.time() - game.last_powerup_time > POWERUP_DURATION:
                    game.powerups.deactivate()
                    game.powerups_active = False
            elif time.time() - game.last_powerup_time > POWERUP_SPAWN_DELAY:
                game.spawn_powerup()


        # TODO Winning condition (8) Check if one player has won the game

    # End the Game
    pygame.quit()
