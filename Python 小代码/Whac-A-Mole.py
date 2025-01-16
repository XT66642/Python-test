 import pygame
import random
import time

# 初始化pygame
pygame.init()

# 设置窗口大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置窗口标题
pygame.display.set_caption('打地鼠')

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# 设置字体
font = pygame.font.SysFont(None, 55)

# 设置地鼠出现的位置
holes = [(100, 100), (300, 100), (500, 100), (100, 300), (300, 300), (500, 300), (100, 500), (300, 500), (500, 500)]

# 设置游戏变量
score = 0
game_over = False
mole_position = random.choice(holes)
mole_time = 0
hit_animation = False
hit_animation_time = 0

# 绘制地鼠
def draw_mole(surface, position, hit=False):
    if hit:
        color = RED
    else:
        color = BROWN
    pygame.draw.circle(surface, color, (position[0] + 50, position[1] + 50), 40)
    pygame.draw.circle(surface, BLACK, (position[0] + 40, position[1] + 40), 5)
    pygame.draw.circle(surface, BLACK, (position[0] + 60, position[1] + 40), 5)
    pygame.draw.polygon(surface, BLACK, [(position[0] + 50, position[1] + 70), (position[0] + 40, position[1] + 90), (position[0] + 60, position[1] + 90)])

# 游戏主循环
clock = pygame.time.Clock()
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mole_position[0] < mouse_x < mole_position[0] + 100 and mole_position[1] < mouse_y < mole_position[1] + 100:
                score += 1
                hit_animation = True
                hit_animation_time = time.time()
                mole_position = random.choice(holes)
                mole_time = time.time()

    # 更新游戏状态
    if not game_over:
        if time.time() - mole_time > 1:
            mole_position = random.choice(holes)
            mole_time = time.time()
        if score >= 10:
            game_over = True

    # 更新反馈动画状态
    if hit_animation and time.time() - hit_animation_time > 0.5:
        hit_animation = False

    # 绘制游戏界面
    screen.fill(WHITE)
    for hole in holes:
        pygame.draw.rect(screen, BLACK, (hole[0], hole[1], 100, 100), 2)
        pygame.draw.rect(screen, BLACK, (hole[0] + 20, hole[1] + 20, 60, 60))
    draw_mole(screen, mole_position, hit_animation)
    score_text = font.render('Score: ' + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))
    if game_over:
        game_over_text = font.render('Game Over', True, RED)
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 25))
        score_text = font.render('Final Score: ' + str(score), True, GREEN)
        screen.blit(score_text, (screen_width // 2 - 100, screen_height // 2 + 25))

    # 更新屏幕显示
    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(60)

# 退出pygame
pygame.quit()
