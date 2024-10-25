import pygame
import random

# ゲームの初期設定
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("ATB Battle System with Pause Option")

# 色の定義 (16進数カラーコードを使用)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

WHITE = hex_to_rgb("#f8f7f6")
BLACK = hex_to_rgb("#000000")
RED = hex_to_rgb("#DA6272")
BLUE = hex_to_rgb("#42AAC7")
GREEN = hex_to_rgb("#C0D860")
GRAY = hex_to_rgb("#808080")

# ゲージとキャラクターの設定
player_atb = 0
enemy_atb = 0
atb_speed_player = 0.5
atb_speed_enemy = 0.4
action_ready = False
pause_on_full = False  # チェックボックスの状態
player_health = 100
enemy_health = 100

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# ボタンとチェックボックスの設定
settings_button = pygame.Rect(20, 350, 100, 30)
checkbox_rect = pygame.Rect(20, 50, 20, 20)
back_button = pygame.Rect(20, 350, 100, 30)

# 画面状態の管理
MAIN_SCREEN = 'main'
SETTINGS_SCREEN = 'settings'
current_screen = MAIN_SCREEN

def draw_main_screen():
    screen.fill(WHITE)
    
    # ATBゲージと体力の描画
    pygame.draw.rect(screen, BLUE, (50, 50, player_atb * 2, 20))
    pygame.draw.rect(screen, RED, (50, 80, player_health * 2, 20))
    pygame.draw.rect(screen, BLUE, (350, 50, enemy_atb * 2, 20))
    pygame.draw.rect(screen, RED, (350, 80, enemy_health * 2, 20))

    # テキストの描画
    player_text = font.render("Player", True, BLACK)
    screen.blit(player_text, (50, 20))
    enemy_text = font.render("Enemy", True, BLACK)
    screen.blit(enemy_text, (350, 20))

    # プレイヤーの体力を数字で表示
    player_health_text = font.render(f"{int(player_health)}/100", True, BLACK)
    screen.blit(player_health_text, (50, 105))

    # Settingsボタンの描画
    pygame.draw.rect(screen, GRAY, settings_button)
    settings_text = font.render("Settings", True, WHITE)
    screen.blit(settings_text, (settings_button.x + 5, settings_button.y + 5))

def draw_settings_screen():
    screen.fill(WHITE)
    
    # 設定画面のタイトル
    title_text = font.render("Settings", True, BLACK)
    screen.blit(title_text, (50, 20))

    # チェックボックスの描画
    pygame.draw.rect(screen, BLACK, checkbox_rect, 2)
    if pause_on_full:
        pygame.draw.rect(screen, GREEN, checkbox_rect.inflate(-4, -4))

    checkbox_text = font.render("Pause on full ATB", True, BLACK)
    screen.blit(checkbox_text, (50, 50))

    # Backボタンの描画
    pygame.draw.rect(screen, GRAY, back_button)
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, (back_button.x + 5, back_button.y + 5))

# メインゲームループ
running = True
while running:
    # イベントの処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == MAIN_SCREEN:
                if settings_button.collidepoint(event.pos):
                    current_screen = SETTINGS_SCREEN
            elif current_screen == SETTINGS_SCREEN:
                if checkbox_rect.collidepoint(event.pos):
                    pause_on_full = not pause_on_full
                elif back_button.collidepoint(event.pos):
                    current_screen = MAIN_SCREEN

    if current_screen == MAIN_SCREEN:
        # ATBゲージの更新（プレイヤーの行動待ち中は停止）
        if player_atb < 100:
            player_atb += atb_speed_player
        else:
            action_ready = True

        # チェックボックスがオンで行動待ちの間、敵のATBを停止
        if not (pause_on_full and action_ready):
            if enemy_atb < 100:
                enemy_atb += atb_speed_enemy
            else:
                player_health -= random.randint(5, 15)
                enemy_atb = 0

        # プレイヤーが行動可能な場合の処理
        if action_ready and pygame.key.get_pressed()[pygame.K_SPACE]:
            enemy_health -= random.randint(10, 20)
            player_atb = 0
            action_ready = False

        draw_main_screen()

        # ゲーム終了判定
        if player_health <= 0 or enemy_health <= 0:
            game_over_text = font.render("Game Over", True, BLACK)
            screen.blit(game_over_text, (200, 180))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
    
    else:  # Settings画面
        draw_settings_screen()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
