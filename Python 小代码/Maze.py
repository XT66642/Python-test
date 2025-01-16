import pygame
import random

# 初始化pygame
pygame.init()

# 设置窗口大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("迷宫游戏")

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# 根据窗口大小计算迷宫的最大尺寸
cell_size = 20
maze_width = screen_width // cell_size
maze_height = screen_height // cell_size

# 定义起点和终点
start = (1, 1)
end = (maze_width - 2, maze_height - 2)

# 生成迷宫
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    stack = [(1, 1)]
    while stack:
        x, y = stack[-1]
        maze[y][x] = 0
        neighbors = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))
        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    # 确保终点周围的单元格不是墙壁
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = end[0] + dx, end[1] + dy
            if 0 <= nx < width and 0 <= ny < height:
                maze[ny][nx] = 0

    return maze

maze = generate_maze(maze_width, maze_height)

# 定义玩家
player = pygame.Rect(start[0] * cell_size, start[1] * cell_size, cell_size, cell_size)

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and maze[player.y // cell_size][player.x // cell_size - 1] == 0:
                player.x -= cell_size
            if event.key == pygame.K_RIGHT and maze[player.y // cell_size][player.x // cell_size + 1] == 0:
                player.x += cell_size
            if event.key == pygame.K_UP and maze[player.y // cell_size - 1][player.x // cell_size] == 0:
                player.y -= cell_size
            if event.key == pygame.K_DOWN and maze[player.y // cell_size + 1][player.x // cell_size] == 0:
                player.y += cell_size

    # 检查是否到达终点
    if player.x == end[0] * cell_size and player.y == end[1] * cell_size:
        print("恭喜你，你赢了！")
        running = False

    # 绘制迷宫
    screen.fill(white)
    for i in range(maze_height):
        for j in range(maze_width):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, black, (j * cell_size, i * cell_size, cell_size, cell_size))
            elif (j, i) == end:
                pygame.draw.rect(screen, green, (j * cell_size, i * cell_size, cell_size, cell_size))

    # 绘制玩家
    pygame.draw.rect(screen, red, player)

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    pygame.time.Clock().tick(30)

# 退出pygame
pygame.quit()
