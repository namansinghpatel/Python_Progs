import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
ORANGE = (255, 165, 0)
BLUE = (0, 102, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
PINK = (255, 192, 203)

# Sun Position
CENTER = (WIDTH // 2, HEIGHT // 2)

# Clock
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)


# Planet Class
class Planet:
    def __init__(self, name, color, radius, distance, speed):
        self.name = name
        self.color = color
        self.radius = radius
        self.distance = distance
        self.angle = 0
        self.speed = speed  # degrees per frame

    def update_position(self):
        self.angle = (self.angle + self.speed) % 360
        rad = math.radians(self.angle)
        self.x = CENTER[0] + self.distance * math.cos(rad)
        self.y = CENTER[1] + self.distance * math.sin(rad)

    def draw_orbit(self):
        pygame.draw.circle(screen, (50, 50, 50), CENTER, self.distance, 1)

    def draw(self):
        self.update_position()
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        label = font.render(self.name, True, WHITE)
        screen.blit(label, (self.x + 8, self.y - 8))


# Create all planets including Pluto
planets = [
    Planet("Mercury", GRAY, 4, 60, 2.5),
    Planet("Venus", ORANGE, 6, 90, 2.0),
    Planet("Earth", BLUE, 6, 120, 1.5),
    Planet("Mars", RED, 5, 150, 1.2),
    Planet("Jupiter", LIGHT_BLUE, 10, 190, 0.9),
    Planet("Saturn", WHITE, 9, 240, 0.6),
    Planet("Uranus", DARK_BLUE, 8, 290, 0.4),
    Planet("Neptune", BROWN, 8, 340, 0.3),
    Planet("Pluto", PINK, 3, 370, 0.2),
]

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    # Draw Sun
    pygame.draw.circle(screen, YELLOW, CENTER, 25)

    # Draw orbits
    for planet in planets:
        planet.draw_orbit()

    # Draw planets
    for planet in planets:
        planet.draw()

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
