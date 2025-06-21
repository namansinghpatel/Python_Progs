import pygame
import math
import sys
import random


# Initialize Pygame
pygame.init()

# Pause control
is_paused = False

# Screen settings
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Solar System Simulator")

# Clock
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 18)

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

# Button settings
button_rect = pygame.Rect(WIDTH - 160, 20, 120, 40)

# Speed control
simulation_speed = 1.0
dragging_slider = False
slider_bar_height = 200
slider_bar_rect = pygame.Rect(WIDTH - 80, 100, 8, slider_bar_height)
slider_knob_rect = pygame.Rect(WIDTH - 88, 100 + slider_bar_height // 2 - 8, 24, 16)


# Planet Class
class Planet:
    def __init__(self, name, color, radius, distance, speed):
        self.name = name
        self.color = color
        self.radius = radius
        self.distance = distance
        self.angle = 0
        self.speed = speed
        self.x = 0
        self.y = 0
        self.revolutions = 0
        self.last_angle = 0

    def update_position(self, speed_multiplier=1.0):
        adjusted_speed = self.speed * speed_multiplier
        self.angle = (self.angle + adjusted_speed) % 360

        if self.last_angle > 350 and self.angle < 10:
            self.revolutions += 1
        self.last_angle = self.angle

        rad = math.radians(self.angle)
        self.x = CENTER[0] + self.distance * math.cos(rad)
        self.y = CENTER[1] + self.distance * math.sin(rad)

    def draw_orbit(self):
        pygame.draw.circle(screen, (50, 50, 50), CENTER, self.distance, 1)

    def draw(self, paused=False, speed_multiplier=1.0):
        if not paused:
            self.update_position(speed_multiplier)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        label = font.render(f"{self.name} ({self.revolutions})", True, WHITE)
        screen.blit(label, (self.x + 8, self.y - 8))


# Create Planets
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

# Generate random star positions
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(500)]
star_colors = [
    (255, 255, 255),
    (144, 238, 144),
    (255, 100, 100),
]  # white, Light Green, Soft Red

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for star in stars:
        base_color = random.choice(star_colors)
        brightness = random.uniform(0.4, 1.0)
        color = tuple(min(255, int(c * brightness)) for c in base_color)
        pygame.draw.circle(screen, color, star, 1)

    # Draw Sun
    pygame.draw.circle(screen, YELLOW, CENTER, 25)

    # Draw orbits and planets
    for planet in planets:
        planet.draw_orbit()
        planet.draw(paused=is_paused, speed_multiplier=simulation_speed)

    # Draw Pause/Play button
    pygame.draw.rect(screen, (80, 80, 80), button_rect, border_radius=10)
    button_label = "Pause" if not is_paused else "Play"
    text = font.render(button_label, True, WHITE)
    screen.blit(text, (button_rect.x + 25, button_rect.y + 10))

    # Draw slider bar and knob
    pygame.draw.rect(screen, WHITE, slider_bar_rect)
    pygame.draw.rect(screen, RED, slider_knob_rect, border_radius=4)

    # Speed label
    speed_label = font.render(f"Speed: {simulation_speed:.1f}x", True, WHITE)
    screen.blit(speed_label, (slider_bar_rect.x - 20, slider_bar_rect.y - 30))

    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                is_paused = not is_paused
            elif slider_knob_rect.collidepoint(event.pos):
                dragging_slider = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_slider = False

        elif event.type == pygame.MOUSEMOTION and dragging_slider:
            new_y = max(
                slider_bar_rect.y,
                min(
                    event.pos[1],
                    slider_bar_rect.y + slider_bar_height - slider_knob_rect.height,
                ),
            )
            slider_knob_rect.y = new_y

            # Convert knob y-position to speed (0.1x to 5x)
            relative_pos = slider_knob_rect.y - slider_bar_rect.y
            slider_range = slider_bar_height - slider_knob_rect.height
            simulation_speed = round(
                5.0 - (relative_pos / slider_range) * (5.0 - 0.1), 1
            )

pygame.quit()
sys.exit()
