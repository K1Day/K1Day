import pygame
import sys
from os import path
 
def run_game():

# Инициализация Pygame
    pygame.init()
    
    # Настройки окна
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sprite Animation")
    
    # Загрузка ресурсов
    def load_image(name, use_alpha=True):
        fullname = path.join('assets', name)
        image = pygame.image.load(fullname)
        return image.convert_alpha() if use_alpha else image.convert()
    
    def load_sprite_sheet(filename, frame_width, frame_height):
        sprite_sheet = load_image(filename)
        num_sprites = sprite_sheet.get_width() // frame_width
        sprites = []
        for i in range(num_sprites):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            sprites.append(frame)
        return sprites
    
    background = load_image("corr.jpg")
    # Масштабирование фона под размер окна
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    door = load_image("door1.png")
    frame_width, frame_height = 126, 126
    idle_sprites = load_sprite_sheet("idle.png", frame_width, frame_height)
    run_sprites = load_sprite_sheet("run.png", frame_width, frame_height)
    
    # Параметры игры
    FPS = 60
    clock = pygame.time.Clock()
    
    # Координаты и скорость персонажа
    x, y = 100, 450
    x_vel = 0
    direction = 'right'  # Начальное направление персонажа
    current_frame = 0
    animation_speed = 0.1
    
    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            x_vel = 5
            direction = 'right'
        elif keys[pygame.K_LEFT]:
            x_vel = -5
            direction = 'left'
        else:
            x_vel = 0
    
        # Обновление позиции персонажа с учетом ограничений экрана
        x += x_vel
        if x > WIDTH - frame_width:
            x = WIDTH - frame_width
        elif x < 0:
            x = 0
    
        # Отрисовка
        screen.blit(background, (0, 0))
        screen.blit(door, (700, 350))  # Позиционирование двери
    
        # Определение и отображение текущего кадра
        if x_vel == 0:
            if direction == 'right':
                screen.blit(idle_sprites[0], (x, y))  # Всегда используем первый кадр для idle
            else:
                # Поворачиваем спрайт idle для направления влево
                flipped_idle_sprite = pygame.transform.flip(idle_sprites[0], True, False)
                screen.blit(flipped_idle_sprite, (x, y))
        else:
            current_frame = (current_frame + animation_speed) % len(run_sprites)
            if direction == 'right':
                screen.blit(run_sprites[int(current_frame)], (x, y))  # Анимация бега вправо
            else:
                # Поворачиваем спрайт бега для направления влево
                flipped_run_sprite = pygame.transform.flip(run_sprites[int(current_frame)], True, False)
                screen.blit(flipped_run_sprite, (x, y))
    
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

def close_game():
    pygame.quit()
    sys.exit()