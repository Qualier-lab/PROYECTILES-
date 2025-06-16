import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puntero Contra Proyectiles")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

player_pos = [WIDTH // 2, HEIGHT // 2]
player_radius = 10

projectiles = []
projectile_speed = 3

bullets = []
bullet_radius = 5
bullet_speed = 7

score = 0
lives = 10  # Vidas iniciales del jugador

def draw_player():
    pygame.draw.circle(screen, GREEN, player_pos, player_radius)

def create_projectile():
    size = random.randint(10, 30)  # Tamaño aleatorio de los proyectiles
    # Generar un punto aleatorio en los bordes de la pantalla
    start_x = random.choice([0, WIDTH])
    start_y = random.choice([0, HEIGHT])
    
    # Calcular la dirección hacia el jugador
    direction = [player_pos[0] - start_x, player_pos[1] - start_y]
    dist = math.sqrt(direction[0] ** 2 + direction[1] ** 2)  # Distancia al jugador
    direction[0] /= dist  # Normalizar la dirección
    direction[1] /= dist  # Normalizar la dirección
    direction[0] *= projectile_speed  # Aplicar velocidad
    direction[1] *= projectile_speed  # Aplicar velocidad
    
    return {'pos': [start_x, start_y], 'dir': direction, 'size': size}

def draw_projectiles():
    for proj in projectiles:
        pygame.draw.circle(screen, RED, (int(proj['pos'][0]), int(proj['pos'][1])), proj['size'])

def update_projectiles():
    global lives
    for proj in projectiles:
        proj['pos'][0] += proj['dir'][0]
        proj['pos'][1] += proj['dir'][1]
        # Verificar si el proyectil se sale de los límites de la pantalla
        if proj['pos'][0] < 0 or proj['pos'][0] > WIDTH or proj['pos'][1] < 0 or proj['pos'][1] > HEIGHT:
            projectiles.remove(proj)
        # Verificar si el proyectil colisiona con el jugador
        if math.sqrt((proj['pos'][0] - player_pos[0]) ** 2 + (proj['pos'][1] - player_pos[1]) ** 2) < player_radius + proj['size']:
            projectiles.remove(proj)
            lives -= 1  # Pierde una vida al ser tocado por un proyectil
            if lives <= 0:
                print("GAME OVER")
                pygame.quit()
                quit()

def create_bullet(mouse_pos):
    angle = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
    direction = [math.cos(angle) * bullet_speed, math.sin(angle) * bullet_speed]
    return {'pos': [player_pos[0], player_pos[1]], 'dir': direction}

def update_bullets():
    global score
    for bullet in bullets:
        bullet['pos'][0] += bullet['dir'][0]
        bullet['pos'][1] += bullet['dir'][1]
        for proj in projectiles:
            dist = math.sqrt((bullet['pos'][0] - proj['pos'][0]) ** 2 + (bullet['pos'][1] - proj['pos'][1]) ** 2)
            if dist < proj['size'] + bullet_radius:
                projectiles.remove(proj)
                bullets.remove(bullet)
                score += 1
                break
        if bullet['pos'][0] < 0 or bullet['pos'][0] > WIDTH or bullet['pos'][1] < 0 or bullet['pos'][1] > HEIGHT:
            bullets.remove(bullet)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, (int(bullet['pos'][0]), int(bullet['pos'][1])), bullet_radius)

def draw_score_and_lives():
    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    lives_text = font.render(f"Vidas: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullets.append(create_bullet(pygame.mouse.get_pos()))
    
    if random.random() < 0.05:
        projectiles.append(create_projectile())
    
    update_projectiles()
    update_bullets()
    
    draw_player()
    draw_projectiles()
    draw_bullets()
    draw_score_and_lives()
    
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
