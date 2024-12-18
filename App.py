import pygame
import random
import sys

# Inicializar o PyGame
pygame.init()

# Configurações da Tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Escape")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Sons
pygame.mixer.init()
sound_enabled = True  # Controle do som
explosion_sound = pygame.mixer.Sound("assets/audio/explosion.wav")
bomb_fall_sound = pygame.mixer.Sound("assets/audio/bomb_fall.wav")  # Som das bombas caindo
bomb_fall_sound.set_volume(0.3)  # Ajuste do volume do som

# Imagens
bomb_image = pygame.image.load("assets/img/bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (50, 70))
player_image = pygame.image.load("assets/img/player.png")
player_image = pygame.transform.scale(player_image, (50, 50))
background_menu_image = pygame.image.load("assets/img/background_menu.png")  # Imagem de fundo do menu
background_menu_image = pygame.transform.scale(background_menu_image, (WIDTH, HEIGHT))
background_game_image = pygame.image.load("assets/img/background.png")  # Imagem de fundo do jogo
background_game_image = pygame.transform.scale(background_game_image, (WIDTH, HEIGHT))
background_gameover_image = pygame.image.load("assets/img/background_gameover.png")  # Imagem de fundo do game over
background_gameover_image = pygame.transform.scale(background_gameover_image, (WIDTH, HEIGHT))

# ícones
sound_on_icon = pygame.image.load("assets/img/sound_on.png")  # Carregar ícone externo
sound_off_icon = pygame.image.load("assets/img/sound_off.png")  # Carregar ícone externo
sound_on_icon = pygame.transform.scale(sound_on_icon, (50, 50))
sound_off_icon = pygame.transform.scale(sound_off_icon, (50, 50))

# Fontes
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Funções Personalizadas
def draw_text(text, font, color, x, y):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(x, y))
    screen.blit(rendered_text, text_rect)

def spawn_enemy(enemy_list, speed):
    x = random.randint(0, WIDTH - 50)
    y = random.randint(-100, -40)
    if sound_enabled:
        bomb_fall_sound.play()  # Toca som da bomba caindo
    enemy_list.append([x, y, speed])

def move_enemies(enemy_list):
    for enemy in enemy_list:
        enemy[1] += enemy[2]  # Move o inimigo para baixo

def check_collision(player_rect, enemies):
    for enemy in enemies:
        if player_rect.colliderect(pygame.Rect(enemy[0], enemy[1], 50, 50)):
            return True
    return False

def game_over_screen(score):
    screen.blit(background_gameover_image, (0, 0))  # Imagem de fundo do game over
    draw_text("GAME OVER", font, RED, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(f"Score: {score}", small_font, WHITE, WIDTH // 2, HEIGHT // 2 + 30)
    draw_text("Press SPACE to Restart", small_font, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        pygame.mixer.unpause()
    else:
        pygame.mixer.pause()

def draw_sound_icon():
    icon = sound_on_icon if sound_enabled else sound_off_icon
    screen.blit(icon, (WIDTH - 60, 10))

# Menu Principal
def main_menu():
    run = True
    while run:
        screen.blit(background_menu_image, (0, 0))  # Desenha a imagem de fundo do menu
        draw_text("Game", font, BLACK, WIDTH // 2, HEIGHT // 2 - 120)
        draw_text("Space Escape", font, BLACK, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text("Press SPACE to Start", small_font, BLACK, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to Exit", small_font, BLACK, WIDTH // 2, HEIGHT // 2 + 50)
        draw_sound_icon()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(WIDTH - 60, 10, 50, 50).collidepoint(event.pos):
                    toggle_sound()

# Game Loop
def game_loop():
    global sound_enabled
    player = pygame.Rect(WIDTH // 2, HEIGHT - 60, 50, 50)
    player_speed = 5

    enemy_list = []
    spawn_timer = 0
    score = 0

    run = True
    while run:
        screen.blit(background_game_image, (0, 0))  # Imagem de fundo do jogo

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(WIDTH - 60, 10, 50, 50).collidepoint(event.pos):
                    toggle_sound()

        # Movimentos do Jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.move_ip(player_speed, 0)

        # Gerenciar Inimigos
        spawn_timer += 1
        if spawn_timer > 30:  # Cria um inimigo a cada 30 frames
            spawn_enemy(enemy_list, random.randint(3, 8))
            spawn_timer = 0
        move_enemies(enemy_list)
        
        # Desenhar Inimigos (bombas)
        for enemy in enemy_list:
            screen.blit(bomb_image, (enemy[0], enemy[1]))

        # Verificar Colisão
        if check_collision(player, enemy_list):
            if sound_enabled:
                explosion_sound.play()
            game_over_screen(score)
            return

        # Atualizar Pontuação
        score += 1
        draw_text(f"Score: {score}", small_font, BLACK, 70, 20)
        draw_sound_icon()

        # Desenhar Jogador (imagem)
        screen.blit(player_image, player)
        pygame.display.update()
        clock.tick(FPS)

# Main
if __name__ == "__main__":
    while True:
        main_menu()
        game_loop()
