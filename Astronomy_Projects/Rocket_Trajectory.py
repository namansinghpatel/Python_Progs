import pygame
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GRAVITY = 9.81  # m/s²
SCALE = 1.5     # Pixels per meter (for visualization)

# Rocket parameters
mass = 500  # kg
thrust = 15000  # N (Newtons)
burn_time = 5  # seconds

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Trajectory Simulator")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)

# Rocket state
altitude = 0
velocity = 0
time_elapsed = 0
path = []
running = True

while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds
    time_elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics
    if time_elapsed <= burn_time:
        acceleration = (thrust / mass) - GRAVITY
    else:
        acceleration = -GRAVITY

    velocity += acceleration * dt
    altitude += velocity * dt

    if altitude < 0:
        altitude = 0
        velocity = 0

    # Store path
    path.append((WIDTH // 2, HEIGHT - int(altitude * SCALE)))

    # Draw
    screen.fill(BLACK)
    for p in path:
        pygame.draw.circle(screen, WHITE, p, 2)

    pygame.draw.rect(screen, RED, (WIDTH // 2 - 5, HEIGHT - int(altitude * SCALE) - 20, 10, 20))

    # HUD
    alt_text = font.render(f"Altitude: {altitude:.1f} m", True, WHITE)
    vel_text = font.render(f"Velocity: {velocity:.1f} m/s", True, WHITE)
    time_text = font.render(f"Time: {time_elapsed:.1f} s", True, WHITE)

    screen.blit(alt_text, (10, 10))
    screen.blit(vel_text, (10, 40))
    screen.blit(time_text, (10, 70))

    pygame.display.flip()

pygame.quit()
