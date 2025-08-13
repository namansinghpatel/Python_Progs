import pygame, random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

stars = [(random.randint(0,800), random.randint(0,600)) for _ in range(100)]
meteors = []

running = True
while running:
    screen.fill((0, 0, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for s in stars:
        pygame.draw.circle(screen, (255, 255, 255), s, 1)
    
    if random.randint(0, 15) == 0:
        meteors.append([random.randint(0,800), 0])
    
    for m in meteors:
        pygame.draw.circle(screen, (255, 200, 100), m, 3)
        m[0] += 5
        m[1] += 3
    
    meteors = [m for m in meteors if m[1] < 600]
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

 
















