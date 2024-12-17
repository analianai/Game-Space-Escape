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
explosion_sound = pygame.mixer.Sound("assets/audio/explosion.wav")
bomb_fall_sound = pygame.mixer.Sound("assets/audio/bomb_fall.wav")  # Som das bombas caindo
bomb_fall_sound.set_volume(0.3)  # Ajuste do volume do som

# Imagens
bomb_image = pygame.image.load("assets/img/bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (50, 50))

# Fontes
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Funções Personalizadas
def draw_text(text, font, color, x, y):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def spawn_enemy(enemy_list, speed):
    x = random.randint(0, WIDTH - 50)
    y = random.randint(-100, -40)
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
    screen.fill(BLACK)
    draw_text("GAME OVER", font, RED, WIDTH // 2 - 150, HEIGHT // 2 - 50)
    draw_text(f"Score: {score}", small_font, WHITE, WIDTH // 2 - 80, HEIGHT // 2 + 30)
    draw_text("Press SPACE to Restart", small_font, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 80)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Menu Principal
def main_menu():
    run = True
    while run:
        screen.fill(BLACK)
        draw_text("Space Escape", font, WHITE, 250, 200)
        draw_text("Press SPACE to Start", small_font, WHITE, 260, 300)
        draw_text("Press ESC to Exit", small_font, WHITE, 270, 350)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False

# Game Loop
def game_loop():
    player = pygame.Rect(WIDTH // 2, HEIGHT - 60, 50, 50)
    player_speed = 5
    player_image = pygame.image.load("assets/img/player.png")  # Substitui o bloco verde por um boneco (imagem PNG)
    player_image = pygame.transform.scale(player_image, (50, 50))

    enemy_list = []
    spawn_timer = 0
    score = 0

    run = True
    while run:
        screen.fill(BLACK)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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
            explosion_sound.play()
            game_over_screen(score)
            return

        # Atualizar Pontuação
        score += 1
        draw_text(f"Score: {score}", small_font, WHITE, 10, 10)

        # Desenhar Jogador (imagem)
        screen.blit(player_image, player)
        pygame.display.update()
        clock.tick(FPS)

# Main
if __name__ == "__main__":
    while True:
        main_menu()
        game_loop()
