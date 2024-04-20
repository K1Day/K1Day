import pygame
from sys import exit
import random
import arka  # Import the arka module
import aaa

def run_ball():
    pygame.init()
    screen = pygame.display.set_mode((1100, 700))
    pygame.display.set_caption('play')
    clock = pygame.time.Clock()
    x = 320
    y = 520
    r = 35
    vel = 20
    door = pygame.image.load("assets//door1.png")
    room = pygame.image.load("assets//home.png")
    phone = pygame.image.load("assets//phone.png")
    student = pygame.image.load("assets//person3.png")

    pygame.mixer_music.load("assets//song.mp3")
    pygame.mixer_music.play(-1)

    # Function to check collision between two circles
    def is_collision(x1, y1, r1, x2, y2, r2):
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance <= r1 + r2

    # Function to check collision between a circle and a rectangular area
    def is_collision_rect(x1, y1, r1, x2, y2, width, height):
        left = x2
        right = x2 + width
        top = y2
        bottom = y2 + height
        
        closest_x = max(left, min(x1, right))
        closest_y = max(top, min(y1, bottom))
        
        distance = ((x1 - closest_x) ** 2 + (y1 - closest_y) ** 2) ** 0.5
        
        return distance < r1

    # Flag to track if a new game has been opened
    open_new_game_flag = False
    open_new_game = False


    # Variable to track time (in seconds)
    timer = 300 # 5 minutes (5 * 60 seconds)
    game_state = "running"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        user = pygame.key.get_pressed()

        # Player movement
        if user[pygame.K_LEFT] and x - vel >= 0 and not is_collision_rect(x - vel, y, r, 0, 320, 280, 700) and not is_collision_rect(x - vel, y, r, 280, 320, 170, 100) and not is_collision_rect(x - vel, y, r, 0, 0, 700, 200) and not is_collision_rect(x - vel, y, r, 800, 420, 700, 100):  
            x -= vel
        if user[pygame.K_RIGHT] and x + vel <= 1100 and not is_collision_rect(x + vel, y, r, 0, 320, 280, 700) and not is_collision_rect(x + vel, y, r, 280, 320, 170, 100) and not is_collision_rect(x + vel, y, r, 0, 0, 700, 200) and not is_collision_rect(x + vel, y, r, 800, 420, 700, 100):  
            x += vel
        if user[pygame.K_UP] and y - vel >= 0 and not is_collision_rect(x, y - vel, r, 0, 320, 280, 700) and not is_collision_rect(x, y - vel, r, 280, 320, 170, 100) and not is_collision_rect(x, y - vel, r, 0, 0, 700, 200) and not is_collision_rect(x, y - vel, r, 800, 420, 700, 100):  
            y -= vel
        if user[pygame.K_DOWN] and y + vel <= 700 and not is_collision_rect(x, y + vel, r, 0, 320, 280, 700) and not is_collision_rect(x, y + vel, r, 280, 320, 170, 100) and not is_collision_rect(x, y + vel, r, 0, 0, 700, 200) and not is_collision_rect(x, y + vel, r, 800, 420, 700, 100):  
            y += vel

        screen.fill((255, 255, 255))
        
        screen.blit(room, (0,0))
        if game_state == "running":
            screen.blit(phone, (400, 400))
        screen.blit(student, (int(x) - student.get_width() // 2, int(y) - student.get_height() // 2))

        if game_state == "running":
            # Check collision with the phone and open a new game if necessary
            if not open_new_game_flag and is_collision(x, y, r, 400, 400, phone.get_width()//2):
                game_state = "arka_running"
                open_new_game_flag = True
                if arka.arka_run(1100, 700):
                    timer += 300  # Add 5 minutes (300 seconds)
                    pygame.mixer_music.pause()
                game_state = "game_over"
        elif game_state == "game_over":
            # Check collision with the door and open a new game if necessary
            if not open_new_game and is_collision(x, y, r, 830, 160, door.get_width()//2):
                aaa.run_game()  # Вызываем функцию открытия новой игры
                open_new_game = True
        
        # Decrease the timer each frame
        timer -= 0.5
        if timer <= 0:
            timer = 0
            
        # Display the timer on the screen
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Time: {int(timer)//60}:{int(timer)%60:02}", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    run_ball()
