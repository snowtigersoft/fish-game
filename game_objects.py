import pygame
import random

import pygame.font

from constants import *


class GameObject:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Fish(GameObject):
    def __init__(self, x, y):
        image = pygame.image.load('assets/fish.png')
        image = pygame.transform.scale(image, (100, 100))
        super().__init__(x, y, image)
        self.speed = FISH_SPEED

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed


class Bubble(GameObject):
    def __init__(self, x, y, letter, max_speed):
        image = pygame.image.load('assets/bubble.png')
        image = pygame.transform.scale(image, (50, 50))
        self.font = pygame.font.Font(None, 50)
        super().__init__(x, y, image)
        self.letter = letter
        self.speed = random.randint(max(1, max_speed - 2), max_speed)
        self.letter_color = RED  # 默认字母颜色为红色
        self.text = self.font.render(self.letter, True, self.letter_color)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = -self.image.get_height()
        self.text = self.font.render(self.letter, True, self.letter_color)  # 渲染字母，颜色使用当前的字母颜色

    def draw(self, screen):
        super().draw(screen)
        text_rect = self.text.get_rect(
            center=(self.x + self.image.get_width() / 2, self.y + self.image.get_height() / 2))
        screen.blit(self.text, text_rect)


class Octopus(GameObject):
    def __init__(self, x, y, max_speed):
        self.image = pygame.image.load('assets/octopus.png')
        # 随机调整章鱼的大小
        octopus_size = random.randint(50, 150)
        self.image = pygame.transform.scale(self.image, (octopus_size, octopus_size))

        super().__init__(x, y, self.image)
        self.speed = random.randint(max(1, max_speed - 2), max_speed)
        self.dx = self.speed
        self.dy = self.speed

    def update(self):
        # 有一定的概率改变移动方向
        if random.random() < 0.02:  # 2% 的概率改变移动方向
            self.dx = random.choice([-1, 1]) * self.speed
            self.dy = random.choice([-1, 1]) * self.speed

        # 更新位置
        self.x += self.dx
        self.y += self.dy

        # 如果章鱼移动到屏幕边缘，就反向移动
        if self.x < 0 or self.x > SCREEN_WIDTH - self.image.get_width():
            self.dx = -self.dx
        if self.y < 0 or self.y > SCREEN_HEIGHT - self.image.get_height():
            self.dy = -self.dy

