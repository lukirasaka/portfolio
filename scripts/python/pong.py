import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
PADDLE_SPEED = 5
DOTTED_LINE_WIDTH = 5

player1_score = 0
player2_score = 0
FONT = pygame.font.Font(None, 36)

def draw_paddle(x, y):
    pygame.draw.rect(WIN, WHITE, pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_ball(x, y):
    pygame.draw.circle(WIN, WHITE, (x, y), BALL_RADIUS)

def draw_dotted_line():
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(WIN, WHITE, pygame.Rect((WIDTH - DOTTED_LINE_WIDTH) // 2, y, DOTTED_LINE_WIDTH, 10))

def draw_scores():
    score_text = FONT.render(f"{player1_score} - {player2_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 50))
    WIN.blit(score_text, score_rect)

def main():
    global player1_score, player2_score

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    paddle1_y = (HEIGHT - PADDLE_HEIGHT) // 2
    paddle2_y = (HEIGHT - PADDLE_HEIGHT) // 2

    ball_dx = random.choice([-1, 1])
    ball_dy = random.choice([-1, 1])

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1_y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            paddle1_y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            paddle2_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            paddle2_y += PADDLE_SPEED

        ball_x += BALL_SPEED_X * ball_dx
        ball_y += BALL_SPEED_Y * ball_dy

        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
            ball_dy *= -1

        if ball_x - BALL_RADIUS <= PADDLE_WIDTH and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT:
            ball_dx *= -1
        elif ball_x + BALL_RADIUS >= WIDTH - PADDLE_WIDTH and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT:
            ball_dx *= -1

        if ball_x < 0:
            player2_score += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
        elif ball_x > WIDTH:
            player1_score += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2

        WIN.fill(BLACK)
        draw_paddle(0, paddle1_y)
        draw_paddle(WIDTH - PADDLE_WIDTH, paddle2_y)
        draw_ball(ball_x, ball_y)
        draw_dotted_line()
        draw_scores()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()