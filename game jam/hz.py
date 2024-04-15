import pygame
import sys
from os import listdir
from os.path import isfile, join

pygame.init()

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
dm = pygame.image.load("corr.jpg").convert_alpha()

FPS = 60

def flip(sprites):
    return [pygame.transform.flip(sprite,True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0 , width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    
    return all_sprites


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1 
    SPRITES = load_sprite_sheets("MainCharacter", "h", 32, 32, True)
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x,y,width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.screen_width = WIDTH


    def move(self, dx, dy):
        new_x = self.rect.x + dx
        if 0 <= new_x <= self.screen_width - self.rect.width:  # Проверка на границы экрана
            self.rect.x = new_x
        self.rect.y += dy
        

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        #self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    
    def draw(self, win):
       
        win.blit(self.sprite,(self.rect.x, self.rect.y))

def handle_move(player, keys):
    if keys[pygame.K_LEFT]:
        player.move_left(5)
    elif keys[pygame.K_RIGHT]:
        player.move_right(5)
    else:
        player.x_vel = 0

def main(window):
    clock = pygame.time.Clock()
    player = Player(100,550,50,50)
    run = True
    while run:
        clock.tick(FPS)
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Получение нажатых клавиш
        keys = pygame.key.get_pressed()

        # Обработка движения игрока
        handle_move(player, keys)

        # Обновление позиции игрока
        player.loop(FPS)

        # Отрисовка фона и объектов
        window.fill(BG_COLOR)
        window.blit(dm, (0, 0))
        player.draw(window)

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(window)
