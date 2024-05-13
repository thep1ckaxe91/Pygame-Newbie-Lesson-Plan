import pygame, random


pygame.init()
WIDTH,HEIGHT = 800,600
window  = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()



def update(dt):
    


def draw():
    pass

if __name__ == "__main__":
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        update(clock.tick(60)/1000)
        draw()
        pygame.display.flip()
        