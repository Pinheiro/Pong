
# This code is based on https://github.com/techwithtim/Pong-Python by Tim Ruscia
# https://www.youtube.com/watch?v=vVGTZlnnX3U

# TO DO
# increase the horizontal (x) speed of the ball after it hits the paddles a few times
# move the angle function into the ball class

# NEW GAME
# Reverse Pong : The left paddle bounces the ball when the ball is near the right border of the window and vice-versa

import pygame
import const
from paddle import Paddle
from ball import Ball

pygame.init()
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WIN = pygame.display.set_mode((const.WIN_WIDTH, const.WIN_HEIGHT))
pygame.display.set_caption("Pong")

def angle(paddle, ball):                            # calculates a new vertical speed for the ball
    diff = (paddle.y + paddle.height / 2) - ball.y  # the ball hits the paddle at this height
    factor = (paddle.height / 2) / ball.MAX_SPEED   # relation between the paddle hight and the ball maximum speed
    return -1 * diff / factor                       # the new vertical speed is faster the closer the ball hits the top or the bottom of the paddle

def main():
    running = True
    clock = pygame.time.Clock()
    left = Paddle(10, const.WIN_HEIGHT//2 - const.PADDLE_HEIGHT //2, const.PADDLE_WIDTH, const.PADDLE_HEIGHT)
    right = Paddle(const.WIN_WIDTH - 10 - const.PADDLE_WIDTH, const.WIN_HEIGHT //2 - const.PADDLE_HEIGHT//2, const.PADDLE_WIDTH, const.PADDLE_HEIGHT)
    ball = Ball(const.WIN_WIDTH // 2, const.WIN_HEIGHT // 2, const.BALL_RADIUS)

    while running:
        clock.tick(const.FPS)
        
        # draw
        
        WIN.fill(const.COLOR_BLACK)                                                                 # background
        left_score_text = SCORE_FONT.render(f"{left.score}", 1, const.COLOR_WHITE)                  # left score
        WIN.blit(left_score_text, (const.WIN_WIDTH//4 - left_score_text.get_width()//2, 20))
        left.draw(WIN)                                                                              # left paddle
        right_score_text = SCORE_FONT.render(f"{right.score}", 1, const.COLOR_WHITE)                # right score
        WIN.blit(right_score_text, (const.WIN_WIDTH * (3/4) - right_score_text.get_width()//2, 20))
        right.draw(WIN)                                                                             # right paddle
        for i in range(10, const.WIN_HEIGHT, const.WIN_HEIGHT//10):                                 # middle line
            if i % 2 != 1:
                pygame.draw.rect(WIN, const.COLOR_WHITE, (const.WIN_WIDTH//2 - 5, i, 10, const.WIN_HEIGHT//20))
        ball.draw(WIN)                                                                              # ball
        pygame.display.update()

        # exit the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        # move paddles
        
        keys = pygame.key.get_pressed()               # detect what key is pressed
        if keys[pygame.K_w]: left.move(up=True)       # <w> moves left paddle up
        if keys[pygame.K_s]: left.move(down=True)     # <s> moves left paddle down
        if keys[pygame.K_UP]: right.move(up=True)     # <keypad up> moved right paddle up
        if keys[pygame.K_DOWN]: right.move(down=True) # <keypad down> moved right paddle down

        ball.move() # move the ball

        # collision detection (bouncing the ball)

        # the ball must bounce of the bottom of the window
        if ball.y + ball.radius >= const.WIN_HEIGHT:
            ball.y_speed *= -1
        
        # the ball must bounce of the top of the window
        if ball.y - ball.radius <= 0:
            ball.y_speed *= -1
        
        # the ball must bounce of the left paddle
        if (ball.x_speed < 0                                    # if the ball is moving to the left
        and ball.y >= left.y and ball.y <= left.y + left.height # and the ball is within the left paddle height
        and ball.x - ball.radius <= left.x + left.width):       # and the ball is at the left paddle then
            ball.x_speed *= -1                                  #     change the ball direction
            ball.y_speed = angle(left, ball)                    #     change the ball angle
        
        # the ball must bounce of the right paddle
        if (ball.x_speed > 0                                       # if the ball is moving to the right
        and ball.y >= right.y and ball.y <= right.y + right.height # and the ball is within the right paddle height
        and ball.x + ball.radius >= right.x):                      # and the ball is at the right paddle then
            ball.x_speed *= -1                                     #     change the ball direction
            ball.y_speed = angle(right, ball)                      #     change the ball angle
        
        # keep scores

        # right player scores when the ball reaches the left border of the window
        if ball.x < 0:
            right.score += 1
            ball.reset()
        
        # left player scores when the ball reaches the right border of the window
        if ball.x > const.WIN_WIDTH:
            left.score += 1
            ball.reset()

        # end of game, new game starts in 5 seconds

        won = False
        if left.score >= const.WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right.score >= const.WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"
        if won:
            text = SCORE_FONT.render(win_text, 1, const.COLOR_WHITE)
            WIN.blit(text, (const.WIN_WIDTH//2 - text.get_width() //2, const.WIN_HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left.reset()
            right.reset()

    pygame.quit()

if __name__ == '__main__':
    main()