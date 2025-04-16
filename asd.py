import pygame
import sys

WIDTH = 1366
HIDTH = 768

pygame.init()

player = pygame.image.load("images/корабль.png")
icon = pygame.image.load("images/иконка.png")
enemy = pygame.image.load("images/пришелец.png")

pygame.display.set_icon(icon)
pygame.display.set_caption("Space Game")
screen = pygame.display.set_mode((WIDTH, HIDTH))

bg_color = (19, 3, 30)

player_x = 623
player_speed = 5

enemy_x = 100
enemy_y = 130
enemy_speed = 1
direction = "right"
distant_enemy_x = 70

clock = pygame.time.Clock()

running = True
while running:
    
    screen.fill(bg_color)
    screen.blit(player, (player_x, 600))
    for i in range(5):
        if direction == "right":
            enemy_x += enemy_speed
        else:
            enemy_x -= enemy_speed
        if enemy_x + distant_enemy_x * 5 == WIDTH - 200:
            direction = "left"
            enemy_y += 70
        if enemy_x == 100:
            direction = "right"
            enemy_y += 70
        for j in range(3):
            screen.blit(enemy, (enemy_x + distant_enemy_x * i, enemy_y + j * 70))
    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and player_x > 100:
        player_x -= player_speed
    if key[pygame.K_RIGHT] and player_x < WIDTH - 200: 
        player_x += player_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    clock.tick(20)
    pygame.display.update()