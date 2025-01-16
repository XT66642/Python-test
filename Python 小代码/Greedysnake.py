 import pygame
import sys
import random
import time

# 初始化pygame
pygame.init()

# 设置窗口大小
width = 640
height = 480
screen = pygame.display.set_mode((width, height))

# 设置窗口标题
pygame.display.set_caption("贪吃蛇小游戏")

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 设置蛇的初始位置和大小
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
food_spawn = True

# 设置初始方向
direction = 'RIGHT'
change_to = direction

# 设置游戏速度
speed = 15

# 设置分数
score = 0

# 设置字体
font_style = pygame.font.SysFont(None, 35)
score_font = pygame.font.SysFont(None, 35)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def show_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

def gameLoop():
    global direction, change_to, food_spawn, score
    game_over = False
    game_close = False

    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while not game_over:

        while game_close == True:
            screen.fill(black)
            message("Press Q to exit or Press C to start", red)
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
        food_spawn = True

        screen.fill(black)
        pygame.draw.rect(screen, red, [food_pos[0], food_pos[1], 10, 10])
        our_snake(10, snake_body)
        show_score(score)
        pygame.display.update()

        if snake_pos[0] < 0 or snake_pos[0] > width-10 or snake_pos[1] < 0 or snake_pos[1] > height-10:
            game_close = True
        for block in snake_body[1:]:
            if snake_pos == block:
                game_close = True

        time.sleep(1 / speed)

gameLoop()
pygame.quit()
sys.exit()
