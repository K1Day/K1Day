import pygame
import sys
from os import listdir
from os.path import isfile, join
import new
pygame.init()

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
dm = pygame.image.load("corr.jpg").convert_alpha()
door = pygame.image.load("door1.png").convert_alpha()
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
        if 0 <= new_x <= self.screen_width - self.rect.width:  
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
        
# Функция для проверки столкновения
def check_collision(player_rect, door_rect):
    return player_rect.colliderect(door_rect)


def handle_move(player, keys):
    if keys[pygame.K_LEFT]:
        player.move_left(5)
    elif keys[pygame.K_RIGHT]:
        player.move_right(5)
    else:
        player.x_vel = 0

# Функция для открытия нового окна pygame
def open_new_window_pygame():
        new.run_game()  
        


door_rect = door.get_rect(topleft=(900, 450))

def main(window):
    clock = pygame.time.Clock()
    player = Player(100, 550, 50, 50)
    run = True
    open_new_window_flag = False  # Флаг для открытия нового окна
    while run:
        clock.tick(FPS)
        
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        keys = pygame.key.get_pressed()


        handle_move(player, keys)

        
        player.loop(FPS)

        
        window.fill(BG_COLOR)
        window.blit(dm, (0, 0))
        window.blit(door, (900, 450))
        player.draw(window)

       
        pygame.display.flip()

        открытие нового окна
        if not open_new_window_flag and check_collision(player.rect, door_rect):
            open_new_window_pygame()  # Вызов функции открытия нового окна
            open_new_window_flag = True

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(window)

