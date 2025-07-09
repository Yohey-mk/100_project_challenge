# maze_app.py

### === Imports ===
import pygame
from maze_map import maze
from show_goal_message import show_goal_message


### === Helper Functions ===

pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Maze Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font_path = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
font = pygame.font.Font(font_path, 14)

TILE_SIZE = 40
goal = (7, 7) #固定
player_position = (1, 1) #可変

### === App Logic ===
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            px, py = player_position
            if event.key == pygame.K_UP:
                ny = py -1
                nx = px
            elif event.key == pygame.K_DOWN:
                ny = py +1
                nx = px
            elif event.key == pygame.K_LEFT:
                ny = py
                nx = px -1
            elif event.key == pygame.K_RIGHT:
                ny = py
                nx = px +1
            else:
                nx, ny = px, py -1
            
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]):
                if maze[ny][nx] != "#":
                    player_position = (nx, ny)
                

    screen.fill(BLACK)

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, BLACK, rect)

    px, py = player_position
    pygame.draw.rect(screen, (0, 255, 0), (px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    gx, gy = goal
    pygame.draw.rect(screen, (0, 0, 255), (gx * TILE_SIZE, gy * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    if player_position == goal:
        show_goal_message(font, screen, WHITE, WIDTH, HEIGHT)
        running = False
        #msg_surface = font.render("Congratulations!", True, (255,255,255))
        #msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        #screen.blit(msg_surface, msg_rect)
        #pygame.display.flip()
        #pygame.time.delay(3000)
        #waiting = True
        #while waiting:
        #    for event in pygame.event.get():
        #        if event.type == pygame.QUIT:
        #            waiting = False
        #            running = False
        #        elif event.type == pygame.KEYDOWN:
        #            waiting = False
        #            running = False

    pygame.display.flip()




# notes
#🛠 使用する主な Pygame 関数・機能
#	•	pygame.draw.rect() … タイル描画
#	•	pygame.KEYDOWN … 移動操作の処理
#	•	screen.blit() … テキストや画像表示
#	•	pygame.time.Clock() … フレーム管理
