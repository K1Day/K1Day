import pygame
from sys import exit
import random
import arka  # Import the arka module
import aaa
from ball import run_ball  # Импортируем функцию run_ball из файла ball.py

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((1100, 700))
    pygame.display.set_caption('Main Menu')

    # Загрузка изображений для фона меню и кнопок
    menu_background = pygame.image.load("assets//backg1.png")
    start_button = pygame.image.load("assets//start-removebg-preview.png")
    exit_button = pygame.image.load("assets//exit-removebg-preview.png")

    # Определение позиций кнопок
    start_button_pos = (135, 535)  # Фактические координаты для кнопки "Start"
    exit_button_pos = (687, 535)  # Фактические координаты для кнопки "Exit"

    # Создание объектов pygame.Rect для кнопок для обработки нажатий
    start_button_rect = start_button.get_rect(topleft=start_button_pos)
    exit_button_rect = exit_button.get_rect(topleft=exit_button_pos)

    running = True
    while running:
        screen.blit(menu_background, (0, 0))
        screen.blit(start_button, start_button_rect.topleft)
        screen.blit(exit_button, exit_button_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button_rect.collidepoint(mouse_pos):
                    # Запускаем игру с шариком
                    run_ball()  # Вызываем функцию из файла ball.py
                elif exit_button_rect.collidepoint(mouse_pos):
                    # Выходим из игры
                    running = False
                    pygame.quit()
                    exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
