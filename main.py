import pygame
import sys
import random
import time

# 難易度の選択
def select_difficulty():
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption('難易度選択')

    font = pygame.font.Font(None, 36)
    easy_text = font.render('Easy', True, WHITE)
    normal_text = font.render('Normal', True, WHITE)
    hard_text = font.render('Hard', True, WHITE)

    # ボタンの背景色
    button_color = (100, 100, 100)  # 灰色

    running = True
    while running:
        screen.fill(BLACK)

        # ボタンの描画
        easy_button_rect = pygame.draw.rect(screen, button_color, (50, 30, 200, 30))  # Easyボタン
        normal_button_rect = pygame.draw.rect(screen, button_color, (50, 80, 200, 30))  # Normalボタン
        hard_button_rect = pygame.draw.rect(screen, button_color, (50, 130, 200, 30))  # Hardボタン

        # テキストの中央揃えでの描画
        screen.blit(easy_text, easy_text.get_rect(center=easy_button_rect.center))
        screen.blit(normal_text, normal_text.get_rect(center=normal_button_rect.center))
        screen.blit(hard_text, hard_text.get_rect(center=hard_button_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 50 <= x <= 250:
                    if 30 <= y <= 60:
                        return 30  # Easy
                    elif 80 <= y <= 110:
                        return 60  # Normal
                    elif 130 <= y <= 160:
                        return 90  # Hard
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# 色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)

# 難易度選択
mine_count = select_difficulty()

# 難易度選択後にウィンドウサイズを変更
pygame.display.set_mode((600, 600))

# ゲームの初期設定
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('マインスイーパー')

# ゲームの設定
cell_size = 20
num_cells_width = width // cell_size
num_cells_height = height // cell_size

# 背景画像の読み込みとスケール
tile_bg_image = pygame.image.load('img/tile-bg.png')
tile_bg_image = pygame.transform.scale(tile_bg_image, (cell_size, cell_size))

# マインフィールドの生成
field = [[0 for x in range(num_cells_width)] for y in range(num_cells_height)]
mines = []

# マインの配置
while len(mines) < mine_count:
    x = random.randint(0, num_cells_width - 1)
    y = random.randint(0, num_cells_height - 1)
    if (x, y) not in mines:
        mines.append((x, y))
        field[y][x] = -1

        # 周囲のセルの数を更新
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < num_cells_width and 0 <= ny < num_cells_height and field[ny][nx] != -1:
                    field[ny][nx] += 1

# 数字ごとの色の定義
number_colors = {
    1: (0, 0, 247),    # 0000F7
    2: (0, 124, 0),    # 007C00
    3: (236, 31, 31),  # EC1F1F
    4: (0, 0, 124),    # 00007C
    5: (124, 0, 0),    # 7C0000
    6: (0, 124, 124),  # 007C7C
    7: (0, 0, 0),      # 000000
    8: (124, 124, 124) # 7C7C7C
}

# 爆弾の画像を読み込み
bomb_image = pygame.image.load('img/bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (cell_size, cell_size))  # セルサイズに合わせてスケール

# ゲーム開始時のタイムスタンプを取得
start_time = time.time()

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # セルの描画
    for y in range(num_cells_height):
        for x in range(num_cells_width):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            screen.blit(tile_bg_image, rect.topleft)  # 背景画像の描画

            # マインまたは数字の描画
            if field[y][x] == -1:
                screen.blit(bomb_image, rect.topleft)
            elif field[y][x] > 0:
                font = pygame.font.Font(None, 24)
                text = font.render(str(field[y][x]), True, number_colors[field[y][x]])
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    # 経過時間の計算
    elapsed_time = int(time.time() - start_time)

    # 残りの爆弾の数（ここでは単純にmine_countを使用）
    remaining_mines = mine_count

    # 情報表示用のフォント設定
    font = pygame.font.Font(None, 36)

    # 経過時間の表示（左上）
    elapsed_text = font.render(f'Time: {elapsed_time}', True, WHITE)
    screen.blit(elapsed_text, (10, 10))

    # 残りの爆弾の数の表示（右上）
    mines_text = font.render(f'Mines: {remaining_mines}', True, WHITE)
    mines_text_rect = mines_text.get_rect(topright=(width - 10, 10))
    screen.blit(mines_text, mines_text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit

