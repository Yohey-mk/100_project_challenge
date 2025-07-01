# day18_ミニシナリオアプリ.py

### === Imports ===
import pygame
import sys
from scenes import scenes

### === Helper Functions ===
pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Test Window")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font_path = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"
font = pygame.font.Font(font_path, 14)

### === App Logic ===
running = True

scene_list = scenes
current_scene = "intro"

while running:
    screen.fill(BLACK)

    scene_data = scenes[current_scene]
    text = font.render(scene_data["text"], True, WHITE)
    screen.blit(text, (50, 50))

    for i, choice in enumerate(scene_data["choices"]):
        option_text = f"{i + 1}. {choice['label']}"
        text_surface = font.render(option_text, True, WHITE)
        screen.blit(text_surface, (50, 100 + i * 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif scene_data["choices"] == "":
            end_text = "物語はここで終了です。ESCで終了します。"
            end_text_surface = font.render(end_text, True, WHITE)
            screen.blit(end_text_surface, (50, 300))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif pygame.K_1 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_1
                if index < len(scene_data["choices"]):
                    current_scene = scene_data["choices"][index]["next"]


    pygame.display.flip()

pygame.quit()
sys.exit()

### === Run App ===


### === Notes ===
#🎯 Day18のゴール（Pygameシナリオ分岐アドベンチャーゲーム）

#テーマ例：「ある日、森の中で不思議な分岐に出会った」

#✅ Day18の進行ステップ（参考）
#	1.	プロトタイプフェーズ（最小限）
#	•	起動画面 + 開始ボタン
#	•	テキストと選択肢を表示
#	•	キーまたはボタンで次のシーンへ進行
#	•	シナリオ分岐（if文 or データ構造）
#	2.	改良フェーズ（余裕があれば）
#	•	シナリオファイルを外部JSON化（読み込み方式）
#	•	画像背景/キャラの追加
#	•	サウンドエフェクト or BGM
#	3.	発展フェーズ（次のDayへ続けてもOK）
#	•	セーブ・ロード機能
#	•	状態に応じて分岐が変わる（例：持ち物、好感度）
#	•	マルチエンディング

#🧠 学べること
#	•	状態管理（scene, 選択肢、変数の変化）
#	•	イベント処理（キー入力やマウス操作）
#	•	構造化思考（シナリオの木構造や再利用性）
#	•	外部データとの連携（JSONなど）
#	•	Pygameの基本操作（画面更新、文字描画、イベントループ）
#