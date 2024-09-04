import const
import pygame

class Paddle:
    COLOR = const.COLOR_WHITE
    SPEED = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.score = 0

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=False, down=False):
        # move paddle up or down
        if up:
            self.y -= self.SPEED
        if down:
            self.y += self.SPEED
        # keep whole paddle inside the screen
        if self.y < 0:
            self.y = 0
        if self.y > const.WIN_HEIGHT - const.PADDLE_HEIGHT:
            self.y = const.WIN_HEIGHT - const.PADDLE_HEIGHT

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.score = 0
