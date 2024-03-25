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
                        return (300, 300)  # Easy
                    elif 80 <= y <= 110:
                        return (400, 400)  # Normal
                    elif 130 <= y <= 160:
                        return (500, 500)  # Hard
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# 色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)

# 難易度選択
window_size = select_difficulty()

# 難易度選択後にウィンドウサイズを変更
pygame.display.set_mode(window_size)

# ゲームの初期設定
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('マインスイーパー')

# ゲームの設定
cell_size = 20
num_cells_width = window_size[0] // cell_size
num_cells_height = window_size[1] // cell_size

# 背景画像の読み込みとスケール
tile_bg_image = pygame.image.load('img/tile-bg.png').convert()
tile_bg_image = pygame.transform.scale(tile_bg_image, (cell_size, cell_size))

# マインフィールドの生成
field = [[0 for x in range(num_cells_width)] for y in range(num_cells_height)]
opened = [[False for x in range(num_cells_width)] for y in range(num_cells_height)]  # 各セルの開閉状態を追跡
flags = [[False for x in range(num_cells_width)] for y in range(num_cells_height)]  # 各セルのフラグマーク状態を追跡
mines = []

# マインの配置
mine_count = 40  # Easyの場合のマインの数
if window_size == (400, 400):  # Normal
    mine_count = 70
elif window_size == (500, 500):  # Hard
    mine_count = 100

mines_placed = False  # ゲーム開始時にはマインは配置されていない

def place_mines(first_click_pos, mine_count, num_cells_width, num_cells_height):
    mines = []
    while len(mines) < mine_count:
        x = random.randint(0, num_cells_width - 1)
        y = random.randint(0, num_cells_height - 1)
        if (x, y) != first_click_pos and (x, y) not in mines:
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

# タイル画像の読み込みとスケール
tile_image = pygame.image.load('img/tile.png')
tile_image = pygame.transform.scale(tile_image, (cell_size, cell_size))

# フラグ画像の読み込みとスケール（透過処理の確認）
flag_image = pygame.image.load('img/flag.png').convert_alpha()
flag_image = pygame.transform.scale(flag_image, (cell_size, cell_size))

# ゲーム開始時のタイムスタンプと経過時間の固定値を保持する変数を定義
start_time = time.time()
fixed_elapsed_time = None  # 爆弾を踏んだ時点の経過時間を保持する変数

def open_cell(x, y):
    global mines_placed, fixed_elapsed_time
    if not mines_placed:
        place_mines((x, y), mine_count, num_cells_width, num_cells_height)
        mines_placed = True
    if 0 <= x < num_cells_width and 0 <= y < num_cells_height:
        if not opened[y][x] and not flags[y][x]:
            opened[y][x] = True
            if field[y][x] == -1:  # 爆弾がある場合
                reveal_all_mines()  # すべての爆弾を表示する関数を呼び出す
                fixed_elapsed_time = int(time.time() - start_time)  # 爆弾を踏んだ時点の経過時間を固定
            elif field[y][x] == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx != 0 or dy != 0:
                            open_cell(x + dx, y + dy)

def reveal_all_mines():
    global fixed_elapsed_time  # グローバル変数を関数内で使用する宣言
    for y in range(num_cells_height):
        for x in range(num_cells_width):
            opened[y][x] = True  # すべてのセルを開く
            if field[y][x] == -1:  # セルが爆弾を含む場合
                # 爆弾のあるセルの背景を赤くする
                rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, (255, 0, 0), rect)
    # 爆弾を踏んだ時点の経過時間を固定
    fixed_elapsed_time = int(time.time() - start_time)

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            cell_x, cell_y = x // cell_size, y // cell_size
            if event.button == 1:  # 左クリック
                if not flags[cell_y][cell_x]:  # フラグがない場合のみ開く
                    open_cell(cell_x, cell_y)  # 再帰的にセルを開く
            elif event.button == 3:  # 右クリック
                # 残りの旗の数を計算
                remaining_flags = mine_count - sum(flags[y][x] for y in range(num_cells_height) for x in range(num_cells_width))
                remaining_flags = max(0, remaining_flags)  # 残りの旗の数がマイナスにならないようにする
                if not opened[cell_y][cell_x] and not flags[cell_y][cell_x] and remaining_flags > 0:  # 旗を置く
                    flags[cell_y][cell_x] = True
                elif flags[cell_y][cell_x]:  # 旗を取り除く
                    flags[cell_y][cell_x] = False

    screen.fill(BLACK)

    # セルの描画
    for y in range(num_cells_height):
        for x in range(num_cells_width):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            if not opened[y][x]:  # セルが閉じている場合
                screen.blit(tile_bg_image, rect.topleft)  # 背景画像を描画
                screen.blit(tile_image, rect.topleft)  # tile.pngを常に表示
                if flags[y][x]:  # フラグが置かれている場合
                    screen.blit(flag_image, rect.topleft)  # flag.pngをtile.pngの上に表示
            else:
                # セルが開かれた場合でも背景画像を描画
                screen.blit(tile_bg_image, rect.topleft)
                
                if field[y][x] == -1:  # セルが爆弾を含む場合
                    screen.blit(bomb_image, rect.topleft)
                elif field[y][x] > 0:  # セルが数字を含む場合
                    font = pygame.font.Font(None, 24)
                    text = font.render(str(field[y][x]), True, number_colors[field[y][x]])
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)

    # 経過時間の計算（爆弾を踏んでいない場合は現在の経過時間を計算し、踏んだ場合は固定された経過時間を使用）
    if fixed_elapsed_time is None:
        elapsed_time = int(time.time() - start_time)
    else:
        elapsed_time = fixed_elapsed_time

    # 残りの旗の数の計算
    remaining_flags = mine_count - sum(flags[y][x] for y in range(num_cells_height) for x in range(num_cells_width))
    remaining_flags = max(0, remaining_flags)  # 残りの旗の数がマイナスにならないようにする

    # 情報表示用のフォント設定
    font = pygame.font.Font(None, 36)

    # 経過時間の表示（左上）
    minutes, seconds = divmod(elapsed_time, 60)
    elapsed_text = font.render(f'Time: {minutes:02d}:{seconds:02d}', True, WHITE)
    screen.blit(elapsed_text, (10, 10))
    
    # 残りの旗の数の表示（右上）
    flags_text = font.render(f'Flags: {remaining_flags}', True, WHITE)
    flags_text_rect = flags_text.get_rect(topright=(window_size[0] - 10, 10))
    screen.blit(flags_text, flags_text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit
