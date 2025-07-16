# catch_game.py

### === Imports ===
import pygame
from show_catch_message import show_catch_message, show_miss_message
import random
from game_over import game_over
from settings import WIDTH, HEIGHT, tile_size, font_path,FPS, WHITE, BLACK, RED, BLUE
from sprites import Player, FallingObject

### === Settings ===
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Me if You Can!")


font = pygame.font.Font(font_path, 14)
game_over_font = pygame.font.Font(font_path, 24)

player_img = pygame.image.load("player.png").convert_alpha()
falling_obj_img = pygame.image.load("pizza.png").convert_alpha()

clock = pygame.time.Clock()
#player_position = [1, 10] #リストにしてプレイヤーの位置をミュータブルに。
falling_object = [5, 1]

### === Helper Function ===
def rand_fall():
    falling_object[0] = random.randint(0, WIDTH // tile_size - 1)
    falling_object[1] = 0

### === Sprites ===

all_sprites = pygame.sprite.Group()
player = Player(player_img, [1, 10])
falling = FallingObject(falling_obj_img)
all_sprites.add(player, falling)


### === App Logic ===
running = True
score = 0
player_life = 3
message = ""
message_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            #if event.key == pygame.K_LEFT and player_position[0] > 0:
            #    player_position[0] -= 1
            #elif event.key == pygame.K_RIGHT and player_position[0] < WIDTH // tile_size - 1:
            #    player_position[0] += 1

    clock.tick(FPS)
    screen.fill(BLACK)
    all_sprites.update()

    #falling_object[1] += 0.08

    if pygame.sprite.collide_rect(player, falling):
    #if int(falling_object[1]) == player_position[1] and falling_object[0] == player_position[0]:
        #print("Catch!") -> show_messageモジュールで管理 *学びの軌跡として記述残している
        #show_catch_message(font, screen, WHITE, WIDTH, HEIGHT) *学びの軌跡として記述残している
        score += 1
        message = "Catch!"
        message_timer = 30
        falling.reset()
        #falling_object[0] = random.randint(0, WIDTH // tile_size - 1) -> DRYの法則に従い、関数化 *学びの軌跡として記述残している
        #rand_fall()
    elif falling.rect.top > HEIGHT:
    #elif falling_object[1] >= HEIGHT // tile_size:
        score -= 1
        player_life -= 1
        message = "Miss!"
        message_timer = 30
        falling.reset()
        #show_miss_message(font, screen, WHITE, WIDTH, HEIGHT) *学びの軌跡として記述残している
        #rand_fall()
        #falling_object[0] = random.randint(0, WIDTH // tile_size - 1) -> DRYの法則に従い、関数化 *学びの軌跡として記述残している


    #legacy: 手動でblit
    #px, py = player_position
    #screen.blit(player_img, (px * tile_size, py * tile_size))
    #pygame.draw.rect(screen, BLUE, (px * tile_size, py * tile_size, tile_size, tile_size))
    #obj_x, obj_y =falling_object
    #screen.blit(falling_obj_img, (obj_x * tile_size, obj_y * tile_size))
    #pygame.draw.rect(screen, RED, (obj_x * tile_size, obj_y * tile_size, tile_size, tile_size))
    all_sprites.draw(screen)

    score_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surface, (10, 10))

    player_life_surface = font.render(f"Life: {player_life}", True, WHITE)
    screen.blit(player_life_surface, (10, 40))

    if message_timer > 0:
        msg_surface = font.render(message, True, WHITE)
        msg_rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(msg_surface, msg_rect)
        message_timer -= 1

    if player_life == 0:
        retry = game_over(game_over_font, screen, WHITE, WIDTH)
        if retry:
            player_life = 3
            score = 0
            rand_fall()
            message = ""
            message_timer = 0
            player.rect_topleft = (1 * tile_size, 10 * tile_size)
        else:
            running = False


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
