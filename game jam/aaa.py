import pygame
import sys
import random
from os import path

def run_game():
    pygame.init()
    
    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sprite Animation")
    
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
    
    background = load_image("background.png")
    bdoor = load_image("bdoor.png")
    book = load_image("book.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    door = load_image("door1.png")
    frame_width, frame_height = 126, 126
    idle_sprites = load_sprite_sheet("idle.png", frame_width, frame_height)
    run_sprites = load_sprite_sheet("run.png", frame_width, frame_height)
    
    FPS = 60
    clock = pygame.time.Clock()
    
    x, y = 100, 350
    x_vel = 0
    direction = 'right'
    current_frame = 0
    animation_speed = 0.1
    
    # Глобальные переменные для позиции и скорости книги
    book_x = random.randint(0, WIDTH - frame_width)
    book_y = 0
    book_speed = 3
    score = 0
    
    def check_collision(player_x, player_y, book_x, book_y):
        if (player_x < book_x + book.get_width() and
            player_x + frame_width > book_x and
            player_y < book_y + book.get_height() and
            player_y + frame_height > book_y):
            return True
        return False
    
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
    
        x += x_vel
        if x > WIDTH - frame_width:
            x = WIDTH - frame_width
        elif x < 0:
            x = 0
    
        # Генерация случайной позиции книги при её появлении вверху
        if book_y >= HEIGHT:
            book_x = random.randint(0, WIDTH - frame_width)
            book_y = 0
    
        # Обновление позиции книги
        book_y += book_speed
    
        # Проверка на столкновение книги с игроком
        if check_collision(x, y, book_x, book_y):
            score += 1
            # После столкновения генерируем новую позицию книги
            book_x = random.randint(0, WIDTH - frame_width)
            book_y = 0
    
        screen.blit(background, (0, 0))
        screen.blit(bdoor, (735, 200))
        screen.blit(book, (book_x, book_y))
    
        if x_vel == 0:
            if direction == 'right':
                screen.blit(idle_sprites[0], (x, y))
            else:
                flipped_idle_sprite = pygame.transform.flip(idle_sprites[0], True, False)
                screen.blit(flipped_idle_sprite, (x, y))
        else:
            current_frame = (current_frame + animation_speed) % len(run_sprites)
            if direction == 'right':
                screen.blit(run_sprites[int(current_frame)], (x, y))
            else:
                flipped_run_sprite = pygame.transform.flip(run_sprites[int(current_frame)], True, False)
                screen.blit(flipped_run_sprite, (x, y))
    
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
    
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
