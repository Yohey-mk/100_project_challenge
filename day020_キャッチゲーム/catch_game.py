# catch_game.py

### === Imports ===
import pygame
from show_catch_message import show_catch_message
import random

### === Settings ===
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Me if You Can!")

font_path = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
font = pygame.font.Font(font_path, 14)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

FPS = 60
clock = pygame.time.Clock()

tile_size = 40
player_position = [1, 10] #リストにしてプレイヤーの位置をミュータブルに。
falling_object = [5, 1]


### === Helper Function ===
def rand_fall():
    falling_object[0] = random.randint(0, WIDTH // tile_size - 1)


### === App Logic ===
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player_position[0] > 0:
                player_position[0] -= 1
            elif event.key == pygame.K_RIGHT and player_position[0] < WIDTH // tile_size - 1:
                player_position[0] += 1

    clock.tick(FPS)
    screen.fill(BLACK)

    falling_object[1] += 0.08
    if falling_object[1] >= HEIGHT // tile_size:
        falling_object[1] = 0
        rand_fall()
        #falling_object[0] = random.randint(0, WIDTH // tile_size - 1) -> DRYの法則に従い、関数化

    if int(falling_object[1]) == player_position[1] and falling_object[0] == player_position[0]:
        #print("Catch!") -> show_messageモジュールで管理
        show_catch_message(font, screen, WHITE, WIDTH, HEIGHT)
        #falling_object[0] = random.randint(0, WIDTH // tile_size - 1) -> DRYの法則に従い、関数化
        rand_fall()

    px, py = player_position
    pygame.draw.rect(screen, BLUE, (px * tile_size, py * tile_size, tile_size, tile_size))
    obj_x, obj_y =falling_object
    pygame.draw.rect(screen, RED, (obj_x * tile_size, obj_y * tile_size, tile_size, tile_size))


    pygame.display.update()





#🧩 ゲーム概要
#	•	上からランダムに落ちてくるアイテム（例：フルーツやボール）を、
#	•	プレイヤーが左右に移動する「かご」や「プレート」でキャッチしていく。
#	•	キャッチできたらスコアが加算され、逃すと減点またはミスカウント。
#	•	一定回数ミスしたらゲームオーバー。
#
#🔧 実装のヒント
#🧑‍🎮 プレイヤーの操作
#	•	横移動のみ（pygame.KEYDOWNで左右キーを検知）
#	•	player_x を調整して pygame.Rect を移動
#
#⬇️ 落ちてくるオブジェクト
#	•	一定間隔で新規生成（ランダムなx座標で）
#	•	毎フレーム y座標 を更新して下に移動
#
#🎯 衝突判定
#	•	player_rect.colliderect(object_rect) で判定
#	•	キャッチ成功時にスコア加算＆オブジェクト削除
#
#📊 スコア・ミス表示
#	•	pygame.font を使って左上にスコアを表示
#	•	ミス数が一定以上になったら Game Over を表示し、終了またはリスタート
