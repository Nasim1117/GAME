import pygame
import random
pygame.init()

wn = pygame.display.set_mode((800,800))
pygame.display.set_caption("Snake Game")

x = 200
y = 200
box = 50

dx = 0
dy = 0

time = pygame.time.Clock()
speed = 4

snake_body = [(x, y)]
snake_length = 1

score = 0
high_score = 0

lives = 3
heart_font = pygame.font.SysFont("Segoe UI Emoji", 35)

font = pygame.font.SysFont(None, 40)
game_over_font = pygame.font.SysFont(None, 80)

# spawn food correctly aligned to grid and below score bar
food_x = random.randrange(0, 800, box)
food_y = random.randrange(box * 2, 800, box)   

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -box
                dy = 0
            if event.key == pygame.K_RIGHT:
                dx = box
                dy = 0
            if event.key == pygame.K_UP:
                dx = 0
                dy = -box 
            if event.key == pygame.K_DOWN:
                dx = 0
                dy = box            

    wn.fill((15,15,25))  
    time.tick(speed)

    x += dx
    y += dy

    # Wall collision
    if x < 0 or x >= 800 or y < box * 2 or y >= 800:
        lives -= 1
        if lives <= 0:
            running = False
        else:
            x = 200
            y = 200
            snake_body = [(x, y)]
            snake_length = 1

    snake_body.append((x, y))

    if len(snake_body) > snake_length:
        snake_body.pop(0)

    # Self collision
    if (x, y) in snake_body[:-1]:
        lives -= 1
        if lives <= 0:
            running = False
        else:
            x = 200
            y = 200
            snake_body = [(x, y)]
            snake_length = 1

    # Food 
    if x == food_x and y == food_y:
        food_x = random.randrange(0, 800, box)
        food_y = random.randrange(box * 2, 800, box)
        snake_length += 1
        score += 1

        if score > high_score:
            high_score = score

    # apple
    pygame.draw.circle(
        wn,
        (255,0,0),
        (food_x + box//2, food_y + box//2),
        box//3
    )

    pygame.draw.rect(
        wn,
        (0,200,0),
        (food_x + box//2 - 3, food_y + 5, 6, 12)
    )

    # Grid lines
    for i in range(0, 800, box):
        pygame.draw.line(wn, (40,40,40), (i,box*2), (i,800))
        pygame.draw.line(wn, (40,40,40), (0,i), (800,i))

    # Border
    pygame.draw.rect(wn, (100,100,120), (0,box*2,800,800-box*2), 5)

    # Snake body
    for part in snake_body[:-1]:
        pygame.draw.rect(wn, (0,200,0), (part[0], part[1], box, box))

    # Snake head
    pygame.draw.rect(wn, (0,255,0), (snake_body[-1][0], snake_body[-1][1], box, box))

    # Snake eyes
    pygame.draw.circle(wn, (0,0,0), (snake_body[-1][0] + 15, snake_body[-1][1] + 15), 5)
    pygame.draw.circle(wn, (0,0,0), (snake_body[-1][0] + 35, snake_body[-1][1] + 15), 5)

    # Score bar
    pygame.draw.rect(wn, (30,30,50), (0,0,800,box*2))
    pygame.draw.line(wn, (80,80,120), (0,box*2), (800,box*2), 2)

    score_text = font.render("Score: " + str(score), True, (255,255,255))
    wn.blit(score_text, (15, 20))

    heart_text = heart_font.render("❤️ " * lives, True, (255,255,255))
    wn.blit(heart_text, (600,15))

    pygame.display.update()

# Game Over Screen
wn.fill((15,15,25))

pygame.draw.rect(wn, (120,120,160), (150,200,500,350), 3)

game_over_text = game_over_font.render("GAME OVER", True, (255,60,60))
game_rect = game_over_text.get_rect(center=(400, 300))
wn.blit(game_over_text, game_rect)

final_score_text = font.render("Your Score: " + str(high_score), True, (255,255,255))
score_rect = final_score_text.get_rect(center=(400, 400))
wn.blit(final_score_text, score_rect)

thank_text = font.render("Thanks for playing!", True, (180,180,200))
thank_rect = thank_text.get_rect(center=(400, 470))
wn.blit(thank_text, thank_rect)

pygame.display.update()
pygame.time.delay(2000)

pygame.quit()
