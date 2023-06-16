#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaochunyou'

import json
import random

import pygame

from constants import *
from game_objects import Fish, Bubble, Octopus


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fish Bubble Game")
        self.fish = Fish(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bubbles = []
        self.octopuses = []
        self.background = pygame.image.load('assets/ocean.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.dx, self.dy = 0, 0
        self.score = 0
        self.target_bubble = None
        self.font = pygame.font.Font(None, 50)
        self.game_over = False
        self.win = False
        self.running = True
        self.start_ticks = pygame.time.get_ticks()
        self.time_left = ROUND_SECONDS
        self.current_level = 0
        self.levels = self.load_levels('levels.json')
        self.init_level(self.levels[self.current_level])

    def load_levels(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def init_level(self, level_config):
        self.bubbles = [Bubble(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                               random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), level_config["bubble_speed"]) for _ in
                        range(level_config["bubble_count"])]
        self.octopuses = [Octopus(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                                  level_config["octopus_speed"]) for _ in range(level_config["octopus_count"])]

    def start_level(self):
        self.target_bubble = None
        self.game_over = False
        self.win = False
        self.time_left = ROUND_SECONDS
        self.start_ticks = pygame.time.get_ticks()
        self.init_level(self.levels[self.current_level])

    def safe_period(self):
        '''
        每个关卡开始前3s是安全时间
        :return:
        '''
        return ROUND_SECONDS - self.time_left < 3

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.dy = -1
            elif event.key == pygame.K_DOWN:
                self.dy = 1
            elif event.key == pygame.K_LEFT:
                self.dx = -1
            elif event.key == pygame.K_RIGHT:
                self.dx = 1
            elif event.key == pygame.K_r and self.game_over:
                self.score = 0
                self.current_level = 0
                self.start_level()
            elif pygame.K_a <= event.key <= pygame.K_z:  # 如果按下的是字母键
                self.target_bubble = pygame.key.name(event.key).lower()  # 将 target_bubble 设置为对应的字母
                # 更改泡泡字母颜色
                for bubble in self.bubbles:
                    if bubble.letter.lower() == self.target_bubble:
                        bubble.letter_color = GREEN
                    else:
                        bubble.letter_color = RED
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.dy = 0
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.dx = 0

    def update(self):
        # 更新倒计时
        if not self.game_over:
            seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000  # 得到已经过去的秒数
            self.time_left = ROUND_SECONDS - seconds  # 计算剩余时间
            if self.time_left <= 0:
                self.game_over = True

    def draw(self):
        screen = self.screen
        fish = self.fish
        # 填充背景颜色
        screen.fill((0, 0, 0))
        # 绘制背景图片
        screen.blit(self.background, (0, 0))
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        # 显示剩余时间
        time_text = self.font.render(f'Time left: {int(self.time_left)}', True, (255, 255, 255))
        screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 20))
        # 显示当前关卡
        level_text = self.font.render(f'Level: {self.current_level + 1}', True, (255, 255, 255))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 20))

        # 更新并绘制每个泡泡和章鱼
        for bubble in self.bubbles:
            if not self.game_over and fish.x < bubble.x < fish.x + fish.image.get_width() and fish.y < bubble.y < fish.y + fish.image.get_height():
                if bubble.letter.lower() == self.target_bubble:  # 如果泡泡的字母与用户指定的字母匹配
                    self.score += 1
                    self.bubbles.remove(bubble)
                    continue
                elif not self.safe_period():  # 如果泡泡的字母与用户指定的字母不匹配
                    self.game_over = True
                    self.win = False
                    break
            bubble.update()
            bubble.draw(screen)
        if len(self.bubbles) == 0:
            self.game_over = True
            self.win = True
        for octopus in self.octopuses:
            octopus.update()
            octopus.draw(screen)
        # 处理鱼和章鱼的碰撞
        if not self.game_over and not self.win and not self.safe_period():  # 仅当游戏未结束并且玩家还未赢得游戏时，章鱼可以使玩家失败
            for octopus in self.octopuses:
                if fish.x < octopus.x < fish.x + fish.image.get_width() and fish.y < octopus.y < fish.y + fish.image.get_height():
                    self.game_over = True
                    self.win = False
                    break
        fish.draw(screen)
        fish.move(self.dx, self.dy)

        if self.game_over:
            if self.win:
                self.current_level += 1
                if self.current_level < len(self.levels):
                    self.start_level()
                else:
                    result_text = self.font.render('You Win the Game!', True, (0, 255, 0))
            else:
                result_text = self.font.render('Game Over!', True, (255, 0, 0))
            if self.game_over:
                screen.blit(result_text, (
                    SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - result_text.get_height() // 2))

        # 更新屏幕
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
