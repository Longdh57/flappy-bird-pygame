import sys
import pygame
import random

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

GRAVITY = 0.25
GAME_ACTIVE = True
bird_movement = 0
score = 0
high_score = 0

bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_position = 0

bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 1
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# Tao timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 500)

# Tao pipe
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tao timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)

# Tao man hinh ket thuc
over_surface = pygame.transform.scale2x(pygame.image.load('assets/gameover.png').convert_alpha())
over_rect = over_surface.get_rect(center=(216, 384))

# Chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_count_down = 100


def draw_floor(floor_img, x_position):
    screen.blit(floor_img, (x_position, 650))
    screen.blit(floor_img, (x_position + 432, 650))


def create_pipe():
    random_pipe_position = random.choice([275, 350, 425])
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_position))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_position - 750))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(ro_bird):
    return pygame.transform.rotozoom(ro_bird, -bird_movement * 3, 1)


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_stage):
    if game_stage == 'main':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_stage == 'over':
        score_surface = game_font.render(f'SCORE: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'HIGH SCORE: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 610))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and GAME_ACTIVE:
                bird_movement = -9
                flap_sound.play()
            if event.key == pygame.K_SPACE and GAME_ACTIVE is False:
                GAME_ACTIVE = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if GAME_ACTIVE:
        # Move bird
        bird_movement += GRAVITY
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # Move pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        # Va cham
        GAME_ACTIVE = check_collision(pipe_list)

        # Tinh diem
        score += 0.01
        score_display('main')
        score_count_down -= 1
        if score_count_down == 0:
            score_sound.play()
            score_count_down = 100

    else:
        screen.blit(over_surface, over_rect)
        high_score = update_score(score, high_score)
        score_display('over')

    # Draw floor
    floor_x_position -= 1
    draw_floor(floor_img=floor, x_position=floor_x_position)
    if floor_x_position < -432:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(90)  # Setup FPS
