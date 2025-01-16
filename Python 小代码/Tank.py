 import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 设置窗口大小
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tank Battle")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 子弹类
class Bullet:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.speed = 10

    def update(self):
        if self.direction == 'UP':
            self.y -= self.speed
        elif self.direction == 'DOWN':
            self.y += self.speed
        elif self.direction == 'LEFT':
            self.x -= self.speed
        elif self.direction == 'RIGHT':
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 5, 5))

# 坦克类
class Tank:
    def __init__(self, x, y, color, speed=5):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.direction = 'UP'
        self.bullets = []

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 40, 40))
        if self.direction == 'UP':
            pygame.draw.rect(screen, self.color, (self.x + 15, self.y - 20, 10, 20))
        elif self.direction == 'DOWN':
            pygame.draw.rect(screen, self.color, (self.x + 15, self.y + 40, 10, 20))
        elif self.direction == 'LEFT':
            pygame.draw.rect(screen, self.color, (self.x - 20, self.y + 15, 20, 10))
        elif self.direction == 'RIGHT':
            pygame.draw.rect(screen, self.color, (self.x + 40, self.y + 15, 20, 10))

    def move(self, direction):
        if direction == 'UP':
            self.y -= self.speed
            self.direction = 'UP'
        elif direction == 'DOWN':
            self.y += self.speed
            self.direction = 'DOWN'
        elif direction == 'LEFT':
            self.x -= self.speed
            self.direction = 'LEFT'
        elif direction == 'RIGHT':
            self.x += self.speed
            self.direction = 'RIGHT'

    def shoot(self):
        if self.direction == 'UP':
            self.bullets.append(Bullet(self.x + 20, self.y - 20, 'UP', self.color))
        elif self.direction == 'DOWN':
            self.bullets.append(Bullet(self.x + 20, self.y + 40, 'DOWN', self.color))
        elif self.direction == 'LEFT':
            self.bullets.append(Bullet(self.x - 20, self.y + 20, 'LEFT', self.color))
        elif self.direction == 'RIGHT':
            self.bullets.append(Bullet(self.x + 40, self.y + 20, 'RIGHT', self.color))

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if 0 <= bullet.x < width and 0 <= bullet.y < height]

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw()

    def is_hit(self, other_bullets):
        for bullet in other_bullets:
            if (self.x < bullet.x < self.x + 40 and self.y < bullet.y < self.y + 40):
                return True
        return False

# 创建坦克
player_tank = Tank(100, 100, RED)
enemy_tank = Tank(700, 500, BLUE, speed=8)  # 提高敌方坦克的移动速度

# 设置敌方坦克射击事件
ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SHOOT_EVENT, 1000)  # 每1000毫秒触发一次

# 计分
score = 0

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_tank.shoot()
        elif event.type == ENEMY_SHOOT_EVENT:
            enemy_tank.shoot()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_tank.move('UP')
    if keys[pygame.K_s]:
        player_tank.move('DOWN')
    if keys[pygame.K_a]:
        player_tank.move('LEFT')
    if keys[pygame.K_d]:
        player_tank.move('RIGHT')

    # 敌方坦克随机移动
    if random.random() < 0.01:  # 每100帧随机移动一次
        enemy_tank.move(random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']))

    # 检查敌方坦克是否被击中
    if enemy_tank.is_hit(player_tank.bullets):
        score += 1
        print(f"Enemy tank destroyed! Score: {score}")
        enemy_tank = Tank(random.randint(0, width - 40), random.randint(0, height - 40), BLUE, speed=8)
        player_tank.bullets = [bullet for bullet in player_tank.bullets if not enemy_tank.is_hit([bullet])]

    # 检查玩家坦克是否被击中
    if player_tank.is_hit(enemy_tank.bullets):
        print("Game Over! Player tank destroyed!")
        running = False

    screen.fill(BLACK)
    player_tank.draw()
    player_tank.update_bullets()
    player_tank.draw_bullets()

    enemy_tank.draw()
    enemy_tank.update_bullets()
    enemy_tank.draw_bullets()

    # 显示分数
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
