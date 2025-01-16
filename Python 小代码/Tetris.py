import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
COLORS = [GREEN, BLUE, RED, YELLOW]
BLACK = (0, 0, 0)

# 设置窗口大小
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 创建屏幕对象
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

# 方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # 长条形
    [[1, 1], [1, 1]],  # 方块形
    [[0, 1, 0], [1, 1, 1]],  # T形
    [[1, 0, 0], [1, 1, 1]],  # J形
    [[0, 0, 1], [1, 1, 1]],  # L形
    [[1, 1, 0], [0, 1, 1]],  # S形
    [[0, 1, 1], [1, 1, 0]]  # Z形
]

# 方块类
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def draw(self, screen):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, (self.x * GRID_SIZE + j * GRID_SIZE, self.y * GRID_SIZE + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def move_down(self):
        self.y += 1

    def rotate(self):
        self.shape = [list(reversed(col)) for col in zip(*self.shape)]

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

# 检查方块是否可以移动或旋转
def check_collision(piece, grid):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                x = piece.x + j
                y = piece.y + i
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or (y >= 0 and grid[y][x]):
                    return True
    return False

# 消除行并计算得分
def clear_rows(grid):
    global score
    for i in range(GRID_HEIGHT):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [0] * GRID_WIDTH)
            score += 1

# 游戏主循环
def main():
    global score
    score = 0
    clock = pygame.time.Clock()
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_piece = Tetromino(random.choice(SHAPES), random.choice(COLORS))
    next_piece = Tetromino(random.choice(SHAPES), random.choice(COLORS))
    game_over = False
    fall_time = 0
    fall_speed = 500  # 方块下落速度，单位为毫秒
    font = pygame.font.SysFont(None, 36)  # 设置字体
    paused = False  # 暂停状态标志

    while not game_over:
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not paused:
                        current_piece.move_left()
                        if check_collision(current_piece, grid):
                            current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    if not paused:
                        current_piece.move_right()
                        if check_collision(current_piece, grid):
                            current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    if not paused:
                        current_piece.move_down()
                        if check_collision(current_piece, grid):
                            current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    if not paused:
                        current_piece.rotate()
                        if check_collision(current_piece, grid):
                            current_piece.shape = [list(reversed(col)) for col in zip(*current_piece.shape)]
                elif event.key == pygame.K_p:
                    paused = not paused  # 切换暂停状态

        if not paused:
            if fall_time > fall_speed:
                current_piece.move_down()
                if check_collision(current_piece, grid):
                    current_piece.y -= 1
                    for i, row in enumerate(current_piece.shape):
                        for j, cell in enumerate(row):
                            if cell:
                                grid[current_piece.y + i][current_piece.x + j] = current_piece.color
                    current_piece = next_piece
                    next_piece = Tetromino(random.choice(SHAPES), random.choice(COLORS))
                fall_time = 0

            clear_rows(grid)

            # 检查游戏是否结束
            if any(grid[0]):
                game_over = True

        screen.fill(WHITE)
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        current_piece.draw(screen)

        # 显示得分
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        if paused:
            pause_text = font.render('PAUSED', True, BLACK)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
