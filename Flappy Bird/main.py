import pygame, os
import typing
from typing import List, Union
from random import randint

pygame.init()
pygame.mixer.init()
SCALE = 2
WIDTH, HEIGHT = 288 * SCALE, 512 * SCALE
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# constant
jump_force = 600
gForce = 1700
bg_speed = 50
bg_speed_multiplier = 3.5
pipe_speed = bg_speed * bg_speed_multiplier
pipe_distance = 108 * SCALE  # pixel gap between 2 obstacle
pipe_gap = 100 * SCALE
pipe_min_height = (
    50 * SCALE
)  # gap that a bottom or top pipe will expose that height or more


base_path = os.path.abspath(__file__).removesuffix(os.path.basename(__file__))
# variable to reset
gameStart = False


bg1 = pygame.transform.scale_by(
    pygame.image.load(base_path + "assets/images/background.png").convert(), SCALE
)
bg2 = bg1.copy()
bg1_rect, bg2_rect = bg1.get_rect(), bg2.get_rect()
bg2_rect.left = bg1_rect.right

ground1 = pygame.transform.scale_by(
    pygame.image.load(base_path + "assets/images/base.png").convert(), SCALE
)
ground2 = ground1.copy()
ground_rect1 = ground1.get_rect()
ground_rect2 = ground2.get_rect()
ground_rect1.bottomleft = 0, HEIGHT
ground_rect2.bottomleft = ground_rect1.bottomright
ground_x1, ground_x2 = ground_rect1.x, ground_rect2.x

bird_img = [
    pygame.transform.scale_by(
        pygame.image.load(base_path + "assets/images/bird-upflap.png").convert(), SCALE
    ),
    pygame.transform.scale_by(
        pygame.image.load(base_path + "assets/images/bird-midflap.png").convert(), SCALE
    ),
    pygame.transform.scale_by(
        pygame.image.load(base_path + "assets/images/bird-downflap.png").convert(),
        SCALE,
    ),
    pygame.transform.scale_by(
        pygame.image.load(base_path + "assets/images/bird-midflap.png").convert(), SCALE
    ),
]
bird_img_id = 0
bird_rect = bird_img[0].get_rect().inflate(-5, -5)
bird_center = pygame.Vector2(WIDTH / 3, HEIGHT / 2)
bird_vel = pygame.Vector2()
bird_rect.center = bird_center
bird_anim_cnt = 0
bird_anim_cd = 0.1
bird_max_angle = 45  # angle which the bird would rotate
bird_min_angle = -90
bird_angle = 0
bird_rotate_speed = 720  # per sec

pipe_img = pygame.transform.scale_by(
    pygame.image.load(base_path + "assets/images/pipe.png").convert(), SCALE
)
pipe_rect = pipe_img.get_rect()
pipes: List[pygame.Vector2] = []  # Vec2 save the topleft of the bottom pipe

instruction_overlay = pygame.transform.scale_by(
    pygame.image.load(base_path + "assets/ui/message.png"), SCALE
)

numbers_img = []
for _, __, files in os.walk(base_path + "assets/ui/numbers/"):
    for file in files:
        numbers_img.append(
            pygame.transform.scale_by(
                pygame.image.load(base_path + "assets/ui/numbers/" + file), SCALE
            )
        )

number_rect = numbers_img[0].get_rect()
score = 0

#sfx
wing_sfx = pygame.mixer.Sound(base_path + "assets/sfx/wing.wav")
hit_sfx = pygame.mixer.Sound(base_path + "assets/sfx/hit.wav")
point_sfx = pygame.mixer.Sound(base_path + "assets/sfx/point.wav")

def game_over():
    global pipes, bird_center, bird_vel, bird_rect, gameStart, score, bird_angle
    score = 0
    gameStart = False
    pipes = []
    bird_center = pygame.Vector2(WIDTH / 3, HEIGHT / 2)
    bird_vel = pygame.Vector2()
    bird_rect.center = bird_center
    bird_angle = 0
    hit_sfx.play()


def draw_score():
    score_str = str(score)
    score_surf = pygame.Surface(
        (len(score_str) * number_rect.w, number_rect.h), pygame.SRCALPHA
    )
    cnt = 0
    for num in score_str:
        index = int(num)
        score_surf.blit(numbers_img[index], (number_rect.w * cnt, 0))
        cnt += 1
    window.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 5 * SCALE))


def spawn_pipe():
    global pipes
    if len(pipes) > 0:
        pipes.append(
            pygame.Vector2(
                pipes[-1].x + pipe_distance + pipe_img.get_width(),
                randint(
                    pipe_min_height + pipe_gap,
                    HEIGHT - pipe_min_height - ground_rect1.h,
                ),
            )
        )
    else:
        pipes.append(
            pygame.Vector2(
                pipe_img.get_width() + WIDTH,
                randint(
                    pipe_min_height + pipe_gap,
                    HEIGHT - pipe_min_height - ground_rect1.h,
                ),
            )
        )


def update_pipe(dt):
    global score
    if len(pipes) == 0 or pipes[-1].x <= WIDTH - pipe_distance - pipe_img.get_width():
        spawn_pipe()

    if len(pipes) > 0:
        for pipe_topleft_bottom in pipes:
            pipe_topleft_bottom.x -= pipe_speed * dt

            if 0 <= bird_rect.left - pipe_topleft_bottom.x <= pipe_speed * dt:
                score += 1
                point_sfx.play()

            if (
                bird_rect.collidelist(
                    [
                        pipe_rect.move(pipe_topleft_bottom),
                        pipe_rect.move(
                            pipe_topleft_bottom
                            - pygame.Vector2(0, pipe_gap + pipe_rect.h)
                        ),
                    ]
                )
                != -1
            ):
                game_over()

            if pipe_topleft_bottom.x + pipe_img.get_width() <= 0:
                pipes.pop(0)


def update(dt):
    global ground_x1, ground_x2, bird_vel, bird_center, bird_rect, bg1_rect, bg2_rect, ground_rect1, bird_angle, ground_rect2, bird_img_id, bird_anim_cnt
    if gameStart:
        bird_vel.y += gForce * dt
        bird_center += bird_vel * dt
        bird_rect.center = bird_center

        if bird_vel.y > 0:
            bird_angle -= bird_rotate_speed * dt / 2
        else:
            bird_angle += bird_rotate_speed * 3 * dt
        bird_angle = pygame.math.clamp(bird_angle, bird_min_angle, bird_max_angle)
        if bird_rect.colliderect(ground_rect1) or bird_rect.colliderect(ground_rect2):
            game_over()

        update_pipe(dt)
    bird_anim_cnt += dt
    if bird_anim_cnt >= bird_anim_cd:
        bird_anim_cnt -= bird_anim_cd
        bird_img_id += 1
        bird_img_id %= len(bird_img)
    bg1_rect.x -= bg_speed * dt
    bg2_rect.x -= bg_speed * dt

    ground_x1 -= pipe_speed * dt
    ground_x2 -= pipe_speed * dt
    ground_rect1.x = ground_x1
    ground_rect2.x = ground_x2

    if bg1_rect.right <= 0:
        bg1_rect.left = bg2_rect.right
    if bg2_rect.right <= 0:
        bg2_rect.left = bg1_rect.right

    if ground_rect1.right <= 0:
        ground_x1 = ground_rect1.left = ground_rect2.right

    if ground_rect2.right <= 0:
        ground_x2 = ground_rect2.left = ground_rect1.right

    if bird_rect.top < 0:
        bird_rect.top = 0
        bird_vel.y = 0
        bird_center.y = bird_rect.centery


def draw():
    window.blit(bg1, bg1_rect)
    window.blit(bg2, bg2_rect)

    # draw pipe here
    for pipe_topleft in pipes:
        window.blit(pipe_img, pipe_topleft)
        window.blit(
            pygame.transform.flip(pipe_img, 0, 1),
            pipe_topleft + pygame.Vector2(0, -pipe_img.get_height() - pipe_gap),
        )

    window.blit(ground1, ground_rect1)
    window.blit(ground2, ground_rect2)

    # draw how to play
    if not gameStart:
        window.blit(
            instruction_overlay,
            (
                WIDTH // 2 - instruction_overlay.get_width() // 2,
                HEIGHT // 2 - 180 * SCALE,
            ),
        )
    else:
        draw_score()
    bird = pygame.transform.rotate(bird_img[bird_img_id], bird_angle)
    window.blit(
        bird, bird_center - pygame.Vector2(bird.get_width() / 3, bird.get_height() / 2)
    )


if __name__ == "__main__":

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    gameStart = 1
                    bird_vel.y = -jump_force
                    wing_sfx.play()

        update(clock.tick(60) / 1000)
        draw()
        pygame.display.flip()
