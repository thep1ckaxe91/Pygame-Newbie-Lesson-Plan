import pygame
from typing import Union, List

pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
cell_size = 20

input_direction = pygame.Vector2()
bodies: List[Union[pygame.Rect, pygame.Vector2]] = [
    [pygame.Rect(400, 300, cell_size, cell_size), input_direction],
    [pygame.Rect(400 + cell_size, 300, cell_size, cell_size), pygame.Vector2()],
    [pygame.Rect(400 + 2 * cell_size, 300, cell_size, cell_size), pygame.Vector2()],
]
body_color = pygame.Color(0, 255, 0)

move_cooldown = 0.15
move_cooldown_cnt = 0


def update(dt: float):
    global bodies, move_cooldown_cnt
    move_cooldown_cnt += dt
    if move_cooldown_cnt >= move_cooldown:
        move_cooldown_cnt -= move_cooldown
        # update position of body
        if input_direction != pygame.Vector2():
            for i in range(len(bodies) - 1, 0, -1):
                bodies[i] = bodies[i - 1].copy()
            
            bodies[0][0].topleft += input_direction


def draw():
    window.fill("black")
    for body in bodies:
        pygame.draw.rect(window, body_color, body[0])


running = True

if __name__ == "__main__":

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    input_direction = pygame.Vector2(0, -cell_size)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    input_direction = pygame.Vector2(0, cell_size)
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    input_direction = pygame.Vector2(-cell_size, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    input_direction = pygame.Vector2(cell_size, 0)

        update(clock.tick(60) / 1000)
        draw()
        pygame.display.flip()
