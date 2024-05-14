import pygame, random, os
pygame.init()
SCALE = 2
WIDTH,HEIGHT = 288*SCALE,512*SCALE
window  = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
#constant
jump_force = 13
gForce = 50
bg_speed = 40
bg_speed_multiplier = 3.5
pole_speed = bg_speed * bg_speed_multiplier
base_path = os.path.abspath(__file__).removesuffix(os.path.basename(__file__))
#variable to reset
gameStart = False


bg1 = pygame.transform.scale_by(pygame.image.load(base_path+"assets/images/background.png").convert(),SCALE)
bg2 = bg1.copy()
bg1_rect, bg2_rect = bg1.get_rect(),bg2.get_rect()
bg2_rect.left = bg1_rect.right

ground1 = pygame.transform.scale_by(pygame.image.load(base_path+"assets/images/base.png").convert(),SCALE)
ground2 = ground1.copy()
ground_rect1 = ground1.get_rect()
ground_rect1.bottomleft = 0,HEIGHT
ground_rect2 = ground2.get_rect()
ground_rect2.bottomleft = ground_rect1.bottomright

bird_img = pygame.transform.scale_by(pygame.image.load(base_path+"assets/images/bird-upflap.png").convert(),SCALE)
bird_rect = bird_img.get_rect().inflate(-5,-5)
bird_center = pygame.Vector2(WIDTH/3,HEIGHT/2)
bird_vel = pygame.Vector2()
bird_rect.center = bird_center
def update(dt):
    global bird_vel, bird_center, bird_rect, bg1_rect, bg2_rect, ground_rect1, ground_rect2
    if gameStart:
        bird_vel.y += gForce * dt
        bird_vel.y += bird_vel.y * dt
        bird_center += bird_vel
        bird_rect.center = bird_center

    bg1_rect.x -= bg_speed * dt
    bg2_rect.x -= bg_speed * dt

    ground_rect1.x -= bg_speed * bg_speed_multiplier * dt
    ground_rect2.x -= bg_speed * bg_speed_multiplier * dt

    if bg1_rect.right <= 0:
        bg1_rect.left = bg2_rect.right
    if bg2_rect.right <= 0:
        bg2_rect.left = bg1_rect.right

    if ground_rect1.right <= 0:
        ground_rect1.left = ground_rect2.right
    if ground_rect2.right <= 0:
        ground_rect2.left = ground_rect1.right

    if bird_rect.colliderect(ground_rect1) or bird_rect.colliderect(ground_rect2):
        bird_rect.bottom = ground_rect1.top
        bird_vel.y = 0
def draw():
    window.blit(bg1,bg1_rect)
    window.blit(bg2,bg2_rect)
    window.blit(ground1,ground_rect1)
    window.blit(ground2,ground_rect2)

    window.blit(bird_img,bird_rect.inflate(5,5))

if __name__ == "__main__":
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameStart = 1
                    bird_vel.y = -jump_force
                
        update(clock.tick(60)/1000)
        draw()
        pygame.display.flip()
        