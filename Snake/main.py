import pygame
from random import randint
from typing import Union, List

pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
cell_size = 20

input_direction = pygame.Vector2()
bodies: List[Union[pygame.Rect, pygame.Vector2]] = [
    [pygame.Rect(400, 300, cell_size, cell_size), pygame.Vector2(-cell_size, 0)],
    [
        pygame.Rect(400 + cell_size, 300, cell_size, cell_size),
        pygame.Vector2(-cell_size, 0),
    ],
    [
        pygame.Rect(400 + 2 * cell_size, 300, cell_size, cell_size),
        pygame.Vector2(-cell_size, 0),
    ],
]
body_color = pygame.Color(0, 255, 0)
start = False
move_cooldown = 0.15
move_cooldown_cnt = 0

target = pygame.Rect(
    randint(0, WIDTH // 20) * 20, randint(0, HEIGHT // 20) * 20, cell_size, cell_size
)
target_color = pygame.Color("red")


def reset():
    global input_direction, bodies, start
    start = False
    input_direction = pygame.Vector2()
    bodies = [
        [
            pygame.Rect(400, 300, cell_size, cell_size), 
            pygame.Vector2(-cell_size, 0)
        ],
        [
            pygame.Rect(400 + cell_size, 300, cell_size, cell_size),
            pygame.Vector2(-cell_size, 0),
        ],
        [
            pygame.Rect(400 + 2 * cell_size, 300, cell_size, cell_size),
            pygame.Vector2(-cell_size, 0),
        ],
    ]
    respawn_target()

body_color = pygame.Color(0, 255, 0)
start = False


def respawn_target():
    global bodies, target
    target = pygame.Rect(
        (randint(0, WIDTH // cell_size) - 1) * cell_size,
        (randint(0, HEIGHT // cell_size) - 1) * cell_size,
        cell_size,
        cell_size,
    )
    while target.collidelist([body[0] for body in bodies]) != -1:
        target = pygame.Rect(
            (randint(0, WIDTH // cell_size) - 1) * cell_size,
            (randint(0, HEIGHT // cell_size) - 1) * cell_size,
            cell_size,
            cell_size,
        )

    bodies.append(
        [
            pygame.Rect(*(bodies[-1][0].topleft - bodies[-1][1]), cell_size, cell_size),
            bodies[-1][1].copy(),
        ]
    )


def update_snake():
    global bodies
    bodies[0][1] = input_direction
    for i in range(len(bodies) - 1, -1, -1):
        bodies[i][0].topleft += bodies[i][1]
        bodies[i][0].x %= WIDTH
        bodies[i][0].y %= HEIGHT
    for i in range(len(bodies) - 1, 0, -1):
        bodies[i][1] = bodies[i - 1][1].copy()


def update(dt: float):
    global move_cooldown_cnt, target
    move_cooldown_cnt += dt
    if move_cooldown_cnt >= move_cooldown:
        move_cooldown_cnt -= move_cooldown
        # update position of body
        if start:
            update_snake()

            if bodies[0][0].collidelist([bodies[i][0] for i in range(len(bodies)-1,0,-1)]) != -1:
                reset()

            if bodies[0][0].colliderect(target):
                respawn_target()


def draw():
    window.fill("black")
    pygame.draw.rect(window, target_color, target)
    for body in bodies:
        pygame.draw.rect(window, body_color, body[0])


running = True

if __name__ == "__main__":
    respawn_target()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w] and bodies[0][1].y == 0:
                    input_direction = pygame.Vector2(0, -cell_size)
                    start = True
                elif event.key in [pygame.K_DOWN, pygame.K_s] and bodies[0][1].y == 0:
                    input_direction = pygame.Vector2(0, cell_size)
                    start = True
                elif event.key in [pygame.K_LEFT, pygame.K_a] and bodies[0][1].x == 0:
                    input_direction = pygame.Vector2(-cell_size, 0)
                    start = True
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and bodies[0][1].x == 0:
                    input_direction = pygame.Vector2(cell_size, 0)

        update(clock.tick(60) / 1000)
        draw()
        pygame.display.flip()
