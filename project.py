import pygame
import sys

WIDTH = 1366
HEIGHT = 768

pygame.init()

player = pygame.image.load("images/корабль.png")
icon = pygame.image.load("images/иконка.png")
enemy_png = pygame.image.load("images/пришелец.png")
hp = pygame.image.load("images/жизнь.png")

pygame.display.set_icon(icon)
pygame.display.set_caption("Space Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg_color = (19, 3, 30)

player_x = 623
player_speed = 5
player_hp = 3

enemy_x = 100
enemy_y = 130
enemy_speed = 2
direction = "right"
distant_enemy_x = 70

bullet_speed = 30
clock = pygame.time.Clock()

bullets = []
enemies = []

for i in range(5):
    for j in range(3):
        enemies.append({
            'x': enemy_x + distant_enemy_x * i,
            'y': enemy_y + j * 70,
            'width': 70,
            'height': 50,
            'rect': pygame.Rect(enemy_x + distant_enemy_x * i, enemy_y + j * 70, 70, 50)
        })

running = True
while running:
    screen.fill(bg_color)
    for i in range(player_hp):
        screen.blit(hp, (1200 + 50*i, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(bullets) < 2:
                bullets.append({
                    'x': player_x + 82,
                    'y': 600,
                    'width': 7,
                    'height': 11,
                    'rect': pygame.Rect(player_x + 82, 600, 7, 11)
                })
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 100:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 200: 
        player_x += player_speed

    for enemy in enemies:
        if direction == "right":
            enemy['x'] += enemy_speed
        else:
            enemy['x'] -= enemy_speed
        
        enemy['rect'].x = enemy['x']
        enemy['rect'].y = enemy['y']
    
    if len(enemies) > 0:
        if enemies[-1]['x'] + distant_enemy_x * 4 + enemies[-1]['width'] >= WIDTH + 150:
            direction = "left"
            for enemy in enemies:
                enemy['y'] += 70
        elif enemies[0]['x'] <= 100:
            direction = "right"
            for enemy in enemies:
                enemy['y'] += 70
    else:
        enemy_speed *= 1.5
        direction = 'right'
        for i in range(5):
            for j in range(3):
                enemies.append({
                'x': enemy_x + distant_enemy_x * i,
                'y': enemy_y + j * 70,
                'width': 70,
                'height': 50,
                'rect': pygame.Rect(enemy_x + distant_enemy_x * i, enemy_y + j * 70, 70, 50)
            })

    for bullet in bullets:
        bullet['y'] -= bullet_speed
        bullet['rect'].y = bullet['y']

        if bullet['y'] < 0:
            bullets.remove(bullet)

    screen.blit(player, (player_x, 600))

    for i in enemies:
        screen.blit(enemy_png, (i['x'], i['y']))

    for bullet in bullets:
        pygame.draw.rect(screen, (229, 236, 5), bullet['rect'])
    
    player_rect = pygame.Rect(player_x, 600, 160, 160)
    for enemy in enemies:
        if player_rect.colliderect(enemy['rect']):
            player_hp -= 1
            enemies.clear()
            enemy_speed = 2
            if player_hp == 0:
                running = False

    for bullet in bullets:
        for enemy in enemies:
            if bullet['rect'].colliderect(enemy['rect']):
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                break
    
    pygame.display.update()
    clock.tick(20)

pygame.quit()
sys.exit()