import pygame
pygame.init()
WIDTH, HEIGHT = 800,600
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

gforce = 1500
jump_vel = 500
speed = 500
y_vel = 0
on_ground = False
rect = pygame.Rect(WIDTH/2,HEIGHT/2,50,50)

def update(dt):
    global rect, y_vel, on_ground
    keys = pygame.key.get_pressed()
    y_vel += gforce * dt
    rect.x += keys[pygame.K_d] * speed * dt - keys[pygame.K_a] * speed * dt
    rect.y += y_vel * dt
    if rect.bottom > HEIGHT:
        rect.bottom = HEIGHT
        on_ground = True
        y_vel = 0
    
    if rect.left < 0:
        rect.left = 0
    elif rect.right > WIDTH:
        rect.right = WIDTH

def draw():
    window.fill("black")
    pygame.draw.rect(window,"red",rect)


if __name__ == "__main__":
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
                y_vel = -jump_vel
                on_ground = False
        update(clock.tick(60)/1000)
        draw()
        pygame.display.flip()

    