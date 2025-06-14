import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Balls Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player properties
player_width, player_height = 100, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Ball properties
ball_radius = 10
balls = []
ball_speed = 1.5  # Extremely reduced speed of the balls
spawn_interval = 100  # Further increased interval to drastically reduce ball quantity

# Score
score = 0
lives = 3

# Game loop
running = True
clock = pygame.time.Clock()
frame_count = 0

while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < WIDTH - player_width:
        player_x += player_speed
    
    # Spawn new balls
    if frame_count % spawn_interval == 0:
        balls.append([random.randint(0, WIDTH - ball_radius * 2), 0])
    frame_count += 1
    
    # Move balls and check for collisions
    new_balls = []
    for ball in balls:
        ball[1] += ball_speed
        if ball[1] >= HEIGHT - player_height - 10 and player_x <= ball[0] <= player_x + player_width:
            score += 1  # Ball hit player
        elif ball[1] < HEIGHT:
            new_balls.append(ball)
        else:
            lives -= 1  # Ball hit the floor
    
    balls = new_balls
    
    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    
    # Draw balls
    for ball in balls:
        pygame.draw.circle(screen, RED, (ball[0], ball[1]), ball_radius)
    
    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))
    
    # Game over check
    if lives <= 0:
        running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

