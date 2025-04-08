import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

BACKGROUND_COLOR = (135, 206, 250)

bird_image = pygame.Surface((40, 40))
bird_image.fill((255, 255, 0))

bird_rect = bird_image.get_rect()
bird_rect.x = 50
bird_rect.y = SCREEN_HEIGHT // 2 - bird_rect.height // 2
bird_velocity = 0
gravity = 0.5

pipe_width = 70
pipe_gap = 250
pipe_velocity = 5
pipes = []

pipes_passed = 0
font = pygame.font.Font(None, 36)

pipe_timer = 0
PIPE_INTERVAL = 30
FIRST_PIPE_SPAWN_DELAY = 50

MAX_PIPES = 8

def reset_game():
    global bird_velocity, pipes, pipes_passed, pipe_velocity, PIPE_INTERVAL
    bird_rect.y = SCREEN_HEIGHT // 2 - bird_rect.height // 2
    bird_velocity = 0
    pipes = []
    pipes_passed = 0
    pipe_velocity = 5
    PIPE_INTERVAL = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -6
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                reset_game()

    screen.fill(BACKGROUND_COLOR)

    bird_velocity += gravity
    bird_rect.y += bird_velocity

    for pipe in pipes:
        top_pipe_rect = pygame.Rect(pipe['x'], 0, pipe_width, pipe['gap_y'])
        bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['gap_y'] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe['gap_y'] - pipe_gap)
        pygame.draw.rect(screen, (0, 128, 0), top_pipe_rect)
        pygame.draw.rect(screen, (0, 128, 0), bottom_pipe_rect)
        pipe['x'] -= pipe_velocity

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            reset_game()

        if pipe['x'] < -pipe_width:
            pipes.remove(pipe)

        if pipe['x'] + pipe_width < bird_rect.x and not pipe['passed']:
            pipes_passed += 1
            pipe['passed'] = True
            pipe_velocity += 0.3

    pipe_timer += 1
    if pipe_timer == FIRST_PIPE_SPAWN_DELAY or (pipe_timer >= FIRST_PIPE_SPAWN_DELAY + 1 and pipe_timer >= PIPE_INTERVAL):
        gap_y = random.randint(100, SCREEN_HEIGHT - 100 - pipe_gap)
        if len(pipes) < MAX_PIPES:
            pipes.append({'x': SCREEN_WIDTH, 'gap_y': gap_y, 'passed': False})
            PIPE_INTERVAL = max(50, 100 - pipes_passed * 2)
        pipe_timer = 0

    pygame.draw.rect(screen, (255, 255, 0), bird_rect)

    pipes_passed_text = font.render("Pipes Passed: " + str(pipes_passed), True, (255, 255, 255))
    screen.blit(pipes_passed_text, (20, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()