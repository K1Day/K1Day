import pygame
from sys import exit
import aaa  # Импортируем модуль aaa

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('play')
clock = pygame.time.Clock()
x = 250
y = 250
r = 25
vel = 20
door = pygame.image.load("assets//door1.png")

# Функция для проверки столкновения двух окружностей
def is_collision(x1, y1, r1, x2, y2, r2):
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if distance <= r1 + r2:
        return True
    else:
        return False

# Флаг для отслеживания того, была ли уже открыта новая игра
open_new_game_flag = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    user = pygame.key.get_pressed()

    if user[pygame.K_LEFT]:
        x -= vel
    if user[pygame.K_RIGHT]:
        x += vel
    if user[pygame.K_UP]:
        y -= vel
    if user[pygame.K_DOWN]:
        y += vel

    if x + r > 1000: x = 1000 - r
    if y + r > 800: y = 800 - r
    if x - r < 0: x = r
    if y - r < 0: y = r

    screen.fill((255, 255, 255))
    screen.blit(door, (750, 450))

    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), r)

    # Проверяем столкновение с дверью и открываем новую игру, если необходимо
    if not open_new_game_flag and is_collision(x, y, r, 750, 450, door.get_width()//2):
        aaa.run_game()  # Вызываем функцию открытия новой игры
        open_new_game_flag = True

    pygame.display.update()
    clock.tick(60)

