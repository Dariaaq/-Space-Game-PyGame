import pygame
import pickle
import sys


class Button:
    def __init__(self, x, y, text, width=250, color=(0, 0, 255), hower_color=(100, 100, 255), is_howered=False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.rect = pygame.Rect(x, y, width, 50)
        self.hower_color = hower_color
        self.is_howered = is_howered

    def draw(self, screen, font):
        color = self.hower_color if self.is_howered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=10)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_howered = self.rect.collidepoint(pos)
        return self.is_howered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


def main_menu(cont):

    start_game_button = Button(WIDTH//2 - 100, HEIGHT//2 - 80, 'Начать игру')
    continue_game_button = Button(
        WIDTH//2 - 100, HEIGHT//2 - 80, 'Продолжить игру')
    quit_button = Button(WIDTH//2 - 100, HEIGHT//2, 'Выйти из игры')
    if cont:
        buttons = [continue_game_button, quit_button]
    else:
        buttons = [start_game_button, quit_button]

    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_game_button.is_clicked(mouse_pos, event):
                running = False

            if quit_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()

        for button in buttons:
            button.check_hover(mouse_pos)

        if cont:
            screen.blit(pause_image, (0, 0))
        else:
            screen.blit(start_image, (0, 0))

        for button in buttons:
            button.draw(screen, font)

        pygame.display.update()


def end_game():

    end_game_button = Button(WIDTH//2 - 150, HEIGHT//2 - 80, 'закрыть игру')

    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if end_game_button.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()

        end_game_button.check_hover(mouse_pos)
        screen.blit(end_image, (0, 0))
        end_game_button.draw(screen, font)
        screen.blit(font.render(
            f'Рекорд: {record}', True, (255, 255, 255)), (WIDTH//2 - 100, HEIGHT//2))

        pygame.display.update()


WIDTH = 1366
HEIGHT = 768

pygame.init()

player = pygame.image.load("images/корабль.png")
bg_image = pygame.image.load("images/фон космос.jpg")
icon = pygame.image.load("images/иконка.png")
enemy_png = pygame.image.load("images/пришелец.png")
hp = pygame.image.load("images/жизнь.png")
pause_image = pygame.image.load('images/фон пауза.jpg')
start_image = pygame.image.load('images/фон начало.jpg')
end_image = pygame.image.load('images/фон конец.jpg')

bg_sound = pygame.mixer.Sound('sounds/bg_sound.mp3')
enemy_sound = pygame.mixer.Sound('sounds/enemy_sound.mp3')
fire_sound = pygame.mixer.Sound('sounds/fire_sound.mp3')
conflict_sound = pygame.mixer.Sound('sounds/conflict_sound.mp3')

bg_channel = pygame.mixer.Channel(1)

pygame.display.set_icon(icon)
pygame.display.set_caption("Space Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(size=40)

bg_y = 0

player_x = 623
player_speed = 8
player_hp = 3

enemy_x = 100
enemy_y = 130
enemy_speed = 2
direction = "right"
distant_enemy_x = 70

bullet_speed = 30

clock = pygame.time.Clock()

try:
    with open('record.dat', 'rb') as file:
        record = pickle.load(file)
except:
    record = 0

score = 0
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

main_menu(False)
bg_channel.play(bg_sound)
running = True
while running:

    if not bg_channel.get_busy():
        bg_channel.play(bg_sound)

    bg_y += 1
    if bg_y == HEIGHT:
        bg_y = 0

    screen.blit(bg_image, (0, bg_y))
    screen.blit(bg_image, (0, bg_y-HEIGHT))
    screen.blit(font.render(f'Score: {score}',
                True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f'Record: {record}', True, (255, 255, 255)), (10, 50))
    for i in range(player_hp):
        screen.blit(hp, (1200 + 50*i, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(bullets) < 5:
                fire_sound.play()
                bullets.append({
                    'x': player_x + 82,
                    'y': 600,
                    'width': 7,
                    'height': 11,
                    'rect': pygame.Rect(player_x + 82, 600, 7, 11)
                })
            if event.key == pygame.K_ESCAPE:
                main_menu(True)

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
            if record < score:
                record = score
            score = 0
            conflict_sound.play()
            enemies.clear()
            enemy_speed = 2
            if player_hp == 0:
                with open('record.dat', 'wb') as file:
                    pickle.dump(record, file)
                end_game()

    for bullet in bullets:
        for enemy in enemies:
            if bullet['rect'].colliderect(enemy['rect']):
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                    score += 1
                    enemy_sound.play()
                break

    pygame.display.update()
    clock.tick(20)

pygame.quit()
sys.exit()
