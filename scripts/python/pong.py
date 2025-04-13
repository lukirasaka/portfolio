import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)

BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5
DOTTED_LINE_WIDTH = 5

player1_score = 0
player2_score = 0
FONT = pygame.font.Font(None, 36)

pve_mode = False

# Powerup system
powerups = []
POWERUP_SIZE = 15
POWERUP_INTERVAL = 60 * 5
MAX_POWERUPS = 4

# Fake balls
fake_balls = []

def draw_paddle(x, y):
    pygame.draw.rect(WIN, WHITE, pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_ball(x, y):
    pygame.draw.circle(WIN, WHITE, (x, y), BALL_RADIUS)

def draw_fake_ball(x, y):
    pygame.draw.circle(WIN, WHITE, (x, y), BALL_RADIUS)
    pygame.draw.circle(WIN, MAGENTA, (x, y), 3)

def draw_dotted_line():
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(WIN, WHITE, pygame.Rect((WIDTH - DOTTED_LINE_WIDTH) // 2, y, DOTTED_LINE_WIDTH, 10))

def draw_scores():
    score_text = FONT.render(f"{player1_score} - {player2_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 50))
    WIN.blit(score_text, score_rect)

def draw_mode():
    mode_text = FONT.render("PvE" if pve_mode else "PvP", True, WHITE)
    WIN.blit(mode_text, (10, 10))

def draw_powerups():
    for p in powerups:
        color = RED if p['effect'] == "speed+" else GREEN if p['effect'] == "slow" else MAGENTA
        pygame.draw.rect(WIN, color, p['rect'])

def ai_move(paddle_y, ball_targets, frame_count):
    target = min(ball_targets, key=lambda b: abs(WIDTH - b['x']))
    for b in ball_targets[1:]:
        if abs(b['x'] - WIDTH) < 200 and random.random() < 0.4:
            target = b
    if random.random() < 0.2:
        return paddle_y
    distance_factor = max(1, abs(WIDTH - target['x'])) / WIDTH
    adjusted_speed = int(PADDLE_SPEED * (1.5 - distance_factor))
    error = random.randint(-12, 12)
    center_paddle = paddle_y + PADDLE_HEIGHT // 2
    if center_paddle < target['y'] + error:
        paddle_y += adjusted_speed
    elif center_paddle > target['y'] + error:
        paddle_y -= adjusted_speed
    return max(0, min(HEIGHT - PADDLE_HEIGHT, paddle_y))

def main():
    global player1_score, player2_score, pve_mode, fake_balls

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    paddle1_y = (HEIGHT - PADDLE_HEIGHT) // 2
    paddle2_y = (HEIGHT - PADDLE_HEIGHT) // 2
    ball_dx = random.choice([-1, 1])
    ball_dy = random.choice([-1, 1])
    base_speed = 5
    ball_speed_x = base_speed
    ball_speed_y = base_speed
    speed_timer = 0
    powerup_timer = 0

    clock = pygame.time.Clock()
    running = True
    frame_count = 0

    while running:
        frame_count += 1
        powerup_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_TAB:
                    pve_mode = not pve_mode

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1_y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            paddle1_y += PADDLE_SPEED
        if not pve_mode:
            if keys[pygame.K_UP]:
                paddle2_y -= PADDLE_SPEED
            if keys[pygame.K_DOWN]:
                paddle2_y += PADDLE_SPEED
        else:
            tracked_balls = [{'x': ball_x, 'y': ball_y}] + fake_balls
            paddle2_y = ai_move(paddle2_y, tracked_balls, frame_count)

        paddle1_y = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle1_y))
        paddle2_y = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle2_y))

        ball_x += ball_speed_x * ball_dx
        ball_y += ball_speed_y * ball_dy

        for b in fake_balls:
            b['x'] += ball_speed_x * b['dx']
            b['y'] += ball_speed_y * b['dy']
            if b['y'] - BALL_RADIUS <= 0 or b['y'] + BALL_RADIUS >= HEIGHT:
                b['dy'] *= -1

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
            ball_speed_x = base_speed
            ball_speed_y = base_speed
            speed_timer = 0
            fake_balls.clear()
        elif ball_x > WIDTH:
            player1_score += 1
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = base_speed
            ball_speed_y = base_speed
            speed_timer = 0
            fake_balls.clear()

        # Spawn powerups
        if powerup_timer >= POWERUP_INTERVAL and len(powerups) < MAX_POWERUPS:
            powerup_x = random.randint(WIDTH // 4, WIDTH * 3 // 4)
            powerup_y = random.randint(50, HEIGHT - 50)
            powerup_rect = pygame.Rect(powerup_x, powerup_y, POWERUP_SIZE, POWERUP_SIZE)
            effect = random.choice(["speed+", "slow", "double"])
            powerups.append({'rect': powerup_rect, 'effect': effect})
            powerup_timer = 0

        # Powerup collisions
        for p in powerups[:]:
            expanded_hitbox = p['rect'].inflate(20, 20)
            if expanded_hitbox.collidepoint(ball_x, ball_y):
                if p['effect'] == "speed+":
                    ball_speed_x += 2
                    ball_speed_y += 2
                elif p['effect'] == "slow":
                    ball_speed_x = max(2, ball_speed_x - 2)
                    ball_speed_y = max(2, ball_speed_y - 2)
                elif p['effect'] == "double":
                    new_fake = {
                        'x': ball_x,
                        'y': ball_y,
                        'dx': -ball_dx,
                        'dy': ball_dy
                    }
                    fake_balls.append(new_fake)
                powerups.remove(p)

        # Zrychlení po čase
        speed_timer += 1
        if speed_timer % (60 * 5) == 0:
            ball_speed_x += 0.5
            ball_speed_y += 0.5

        WIN.fill(BLACK)
        draw_paddle(0, paddle1_y)
        draw_paddle(WIDTH - PADDLE_WIDTH, paddle2_y)
        draw_ball(ball_x, ball_y)
        for b in fake_balls:
            draw_fake_ball(int(b['x']), int(b['y']))
        draw_dotted_line()
        draw_scores()
        draw_mode()
        draw_powerups()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
