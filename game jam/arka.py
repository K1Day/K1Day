import pygame
import sys
from random import randrange as rnd

def arka_run(screen_width, screen_height):  # Accept screen width and height as parameters

    fps = 60
    game_score = 0
    paddle_w = 230
    paddle_h = 25
    paddle_speed = 15
    paddle = pygame.Rect(screen_width // 2 - paddle_w // 2, screen_height - paddle_h - 10, paddle_w, paddle_h)
    ball_radius = 20
    ball_speed = 6
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(rnd(ball_rect, screen_width - ball_rect), screen_height // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    breakable_rows = [0, 1, 2]  
    rows = 4
    columns = 10
    block_list = []
    color_list = []

    for j in range(rows):
        for i in range(columns):
            is_breakable = (j == rows - 1 and i == 5) or (j < rows - 1)
            block_rect = pygame.Rect(10 + 110 * i, 10 + 70 * j, 100, 50)
            block_list.append((block_rect, is_breakable))
            if is_breakable:
                color_list.append((rnd(30, 256), rnd(30, 256), rnd(30, 256)))
            else:
                color_list.append((255, 255, 255))

    pygame.init()
    sc = pygame.display.set_mode((screen_width, screen_height))  # Set screen size based on parameters
    clock = pygame.time.Clock()

    def delect_collision(dx, dy, ball, rect, is_breakable):
        if is_breakable:
            pass
        else:
            if dx > 0:
                delta_x = ball.right - rect.left
            else:
                delta_x = rect.right - ball.left
            if dy > 0:
                delta_y = ball.bottom - rect.top
            else:
                delta_y = rect.bottom - ball.top
            
            if abs(delta_x - delta_y) < 10:
                dx, dy = -dx, -dy
            elif delta_x > delta_y:
                dy = -dy
            elif delta_y > delta_x:
                dx = -dx
        return dx, dy

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        sc.fill('black')
        for i, (block, is_breakable) in enumerate(block_list):
            pygame.draw.rect(sc, color_list[i], block)
        pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        if ball.centerx < ball_radius or ball.centerx > screen_width - ball_radius:
            dx = -dx
        if ball.centery < ball_radius:
            dy = -dy

        if ball.colliderect(paddle) and dy > 0:
            dx, dy = delect_collision(dx, dy, ball, paddle, False)
        hit_index = ball.collidelist([block[0] for block in block_list])
        if hit_index != -1:
            hit_rect, is_breakable = block_list[hit_index]
            if is_breakable:
                hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
                pygame.draw.rect(sc, pygame.Color('black'), hit_rect)
                
                game_score += 1
                fps += 2
                block_list.pop(hit_index)
                color_list.pop(hit_index)
                if is_breakable and hit_index == 5:  
                    paddle.width += 50
                    
            else:
                dx, dy = delect_collision(dx, dy, ball, hit_rect, is_breakable)

        # Win, game over
        if ball.bottom > screen_height:
            print(game_score)
            print('GAME OVER')
            return False
        elif not len([block for block, is_breakable in block_list if is_breakable]):
            print(game_score)
            print("WIN!!!!!!!!!!!!!!!!!!!!!!!!!")
            return True
            
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < screen_width:
            paddle.right += paddle_speed

        pygame.display.flip()
        clock.tick(fps)

def close_game():
    pygame.quit()
    sys.exit()


