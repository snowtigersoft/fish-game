import random

import pygame

from constants import GREEN, RED, ROUND_SECONDS, SCREEN_WIDTH, SCREEN_HEIGHT
from game_objects import Fish, Bubble, Octopus

# 初始化 Pygame
pygame.init()
pygame.font.init()

# 设置窗口大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置窗口标题
pygame.display.set_caption("Fish Bubble Game")

# 创建一个小鱼对象
fish = Fish(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# 创建多个 Bubble 和 Octopus 对象
bubbles = [Bubble(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) for _ in range(10)]
octopuses = [Octopus(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(3)]

# 加载背景图片
background = pygame.image.load('assets/ocean.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
dx, dy = 0, 0
score = 0
target_bubble = None  # 用户指定的要吃的泡泡字母

font = pygame.font.Font(None, 50)

game_over = False
win = False

# 游戏主循环
running = True
# 记录游戏开始时间
start_ticks = pygame.time.get_ticks()
# 初始化倒计时
time_left = ROUND_SECONDS
while running:
    # 事件循环
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # 键盘按下事件
            if event.key == pygame.K_UP:
                dy = -1
            elif event.key == pygame.K_DOWN:
                dy = 1
            elif event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_r and game_over:
                score = 0
                target_bubble = None
                game_over = False
                win = False
                # 重置倒计时
                time_left = ROUND_SECONDS
                start_ticks = pygame.time.get_ticks()
                # 创建多个 Bubble 和 Octopus 对象
                bubbles = [Bubble(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                                  random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) for _ in range(10)]
                octopuses = [Octopus(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in
                             range(3)]
            elif pygame.K_a <= event.key <= pygame.K_z:  # 如果按下的是字母键
                target_bubble = pygame.key.name(event.key).lower()  # 将 target_bubble 设置为对应的字母
                # 更改泡泡字母颜色
                for bubble in bubbles:
                    if bubble.letter.lower() == target_bubble:
                        bubble.letter_color = GREEN
                    else:
                        bubble.letter_color = RED
        elif event.type == pygame.KEYUP:  # 键盘松开事件
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                dy = 0
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                dx = 0

    # 更新倒计时
    if not game_over:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # 得到已经过去的秒数
        time_left = ROUND_SECONDS - seconds  # 计算剩余时间
        if time_left <= 0:
            game_over = True

    # 填充背景颜色
    screen.fill((0, 0, 0))
    # 绘制背景图片
    screen.blit(background, (0, 0))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    # 显示剩余时间
    time_text = font.render(f'Time left: {int(time_left)}', True, (255, 255, 255))
    screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 20))

    # 更新并绘制每个泡泡和章鱼
    for bubble in bubbles:
        if not game_over and fish.x < bubble.x < fish.x + fish.image.get_width() and fish.y < bubble.y < fish.y + fish.image.get_height():
            if bubble.letter.lower() == target_bubble:  # 如果泡泡的字母与用户指定的字母匹配
                score += 1
                bubbles.remove(bubble)
                continue
            else:  # 如果泡泡的字母与用户指定的字母不匹配
                game_over = True
                win = False
                break
        bubble.update()
        bubble.draw(screen)
    if len(bubbles) == 0:
        game_over = True
        win = True
    for octopus in octopuses:
        octopus.update()
        octopus.draw(screen)
    # 处理鱼和章鱼的碰撞
    if not game_over and not win:  # 仅当游戏未结束并且玩家还未赢得游戏时，章鱼可以使玩家失败
        for octopus in octopuses:
            if fish.x < octopus.x < fish.x + fish.image.get_width() and fish.y < octopus.y < fish.y + fish.image.get_height():
                game_over = True
                win = False
                break
    fish.draw(screen)
    fish.move(dx, dy)

    if game_over:
        if win:
            result_text = font.render('You Win!', True, (0, 255, 0))
        else:
            result_text = font.render('Game Over!', True, (255, 0, 0))
        screen.blit(result_text, (
        SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - result_text.get_height() // 2))

    # 更新屏幕
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
