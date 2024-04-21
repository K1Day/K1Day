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
    phone = pygame.image.load("assets//phone1.png")
    person_down = pygame.image.load("assets//person3.png")
    person_up = pygame.image.load("assets//up.png")
    person_left = pygame.image.load("assets//left.png")
    person_right = pygame.image.load("assets//right.png")
    note1 = pygame.image.load("assets//note3.png")
    note2 = pygame.image.load("assets//notes.png")
    note3 = pygame.image.load("assets//note2.png")
    pen = pygame.image.load("assets//pen.png")

    pygame.mixer_music.load("assets//song.mp3")
    pygame.mixer_music.play(-1)

    # Flags to track if the notes have been picked up
    note1_picked = False
    note2_picked = False
    note3_picked = False

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

    last_direction = "right"  # Set the initial direction to "right"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        user = pygame.key.get_pressed()

        # Player movement
        if user[pygame.K_LEFT] and x - vel >= 0 and not is_collision_rect(x - vel, y, r, 0, 320, 280, 700) and not is_collision_rect(x - vel, y, r, 280, 330, 250, 100) and not is_collision_rect(x - vel, y, r, 0, 0, 700, 220) and not is_collision_rect(x - vel, y, r, 850, 400, 700, 100):  
            x -= vel
            last_direction = "left"
        elif user[pygame.K_RIGHT] and x + vel <= 1100 and not is_collision_rect(x + vel, y, r, 0, 320, 280, 700) and not is_collision_rect(x + vel, y, r, 280, 330, 250, 100) and not is_collision_rect(x + vel, y, r, 0, 0, 700, 220) and not is_collision_rect(x + vel, y, r, 850, 400, 700, 100):  
            x += vel
            last_direction = "right"
        elif user[pygame.K_UP] and y - vel >= 0 and not is_collision_rect(x, y - vel, r, 0, 320, 280, 700) and not is_collision_rect(x, y - vel, r, 280, 330, 250, 100) and not is_collision_rect(x, y - vel, r, 0, 0, 700, 220) and not is_collision_rect(x, y - vel, r, 850, 400, 700, 100):  
            y -= vel
            last_direction = "up"
        elif user[pygame.K_DOWN] and y + vel <= 700 and not is_collision_rect(x, y + vel, r, 0, 320, 280, 700) and not is_collision_rect(x, y + vel, r, 280, 330, 250, 100) and not is_collision_rect(x, y + vel, r, 0, 0, 700, 220) and not is_collision_rect(x, y + vel, r, 850, 400, 700, 100):  
            y += vel
            last_direction = "down"

        screen.fill((255, 255, 255))
        
        screen.blit(room, (0,0))

        # Display notes if they haven't been picked up
        if not note1_picked:
            screen.blit(note1, (450, 285))
        if not note2_picked:
            screen.blit(note2, (880, 370))
        if not note3_picked:
            screen.blit(note3, (100, 230))

        if game_state == "running":
            screen.blit(phone, (350, 285))

        # Displaying the player based on direction
        if last_direction == "up":
            screen.blit(person_up, (int(x) - person_up.get_width() // 2, int(y) - person_up.get_height() // 2))
        elif last_direction == "down":
            screen.blit(person_down, (int(x) - person_down.get_width() // 2, int(y) - person_down.get_height() // 2))
        elif last_direction == "left":
            screen.blit(person_left, (int(x) - person_left.get_width() // 2, int(y) - person_left.get_height() // 2))
        elif last_direction == "right":
            screen.blit(person_right, (int(x) - person_right.get_width() // 2, int(y) - person_right.get_height() // 2))

        
     
        



        if game_state == "running":
                    if is_collision(x, y, r, 450, 285, note1.get_width() // 2):
                        note1_picked = True
                    if is_collision(x, y, r, 880, 370, note2.get_width() // 2):
                        note2_picked = True
                    if is_collision(x, y, r, 100, 230, note3.get_width() // 2):
                        note3_picked = True
        
            # Check collision with the phone and open a new game if necessary
        if not open_new_game_flag and is_collision(x, y, r, 350, 400, phone.get_width()//2):
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
        
        # Check collision with notes and update note picked flags
        
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
