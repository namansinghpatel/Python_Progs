import pygame
import sys
import random
import time


# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Multiplayer Shooter")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
PLAYER_SIZE = 30
PLAYER_SPEED = 5
BULLET_SPEED = 10
MAX_HEALTH = 5

# Load images
bullet_img = pygame.image.load("bullet.jpg").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (20, 10))

player1_img = pygame.image.load("player1.jpeg").convert_alpha()
player1_img = pygame.transform.scale(player1_img, (PLAYER_SIZE, PLAYER_SIZE))

player2_img = pygame.image.load("player2.jpeg").convert_alpha()
player2_img = pygame.transform.scale(player2_img, (PLAYER_SIZE, PLAYER_SIZE))

# Define walls
walls = [
    pygame.Rect(300, 100, 20, 400),  # Vertical wall
    pygame.Rect(150, 250, 200, 20),  # Horizontal wall
    pygame.Rect(500, 50, 20, 200),  # Maze vertical top
    pygame.Rect(400, 250, 200, 20),  # Maze horizontal middle
    pygame.Rect(600, 250, 20, 300),  # Right vertical wall
    pygame.Rect(100, 500, 250, 20),  # Bottom horizontal
    pygame.Rect(100, 100, 20, 150),  # Top left wall
    pygame.Rect(250, 400, 150, 20),  # Center bottom wall
    pygame.Rect(450, 350, 100, 20),  # Mid right wall
]

SHIELD_SIZE = 40
shield_active = False
shield_rect = pygame.Rect(0, 0, SHIELD_SIZE, SHIELD_SIZE)
shield_spawn_time = pygame.time.get_ticks()
shield_spawn_delay = 30000  # 30 seconds
shield_duration = 10000  # 10 seconds
shield_color = (0, 255, 255)


# Bullet class
class Bullet:
    def __init__(self, x, y, dx, dy):
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Player class
class Player:
    def __init__(self, x, y, image, controls):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.original_image = image
        self.flipped_image = pygame.transform.flip(image, True, False)
        self.image = image
        self.bullets = []
        self.controls = controls
        self.health = MAX_HEALTH
        self.shielded = False
        self.shield_start_time = 0

    def move(self, keys):
        old_position = self.rect.copy()

        if keys[self.controls["up"]] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[self.controls["down"]] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED
        if keys[self.controls["left"]] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
            self.controls["facing"] = "left"
        if keys[self.controls["right"]] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
            self.controls["facing"] = "right"

        # Wall collision
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = old_position
                break

    def shoot(self):
        dx = BULLET_SPEED if self.controls["facing"] == "right" else -BULLET_SPEED
        bullet = Bullet(self.rect.centerx, self.rect.centery, dx, 0)
        self.bullets.append(bullet)

    def draw(self):
        if self.controls["facing"] == "left":
            self.image = self.flipped_image
        else:
            self.image = self.original_image

        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

    def update_bullets(self, opponent):
        for bullet in self.bullets[:]:
            bullet.update()

            # Out of bounds
            if not screen.get_rect().colliderect(bullet.rect):
                self.bullets.remove(bullet)
                continue

            # Hit wall
            if any(bullet.rect.colliderect(wall) for wall in walls):
                self.bullets.remove(bullet)
                continue

            # Hit opponent
            if bullet.rect.colliderect(opponent.rect):
                if not opponent.shielded:
                    opponent.health -= 1
                self.bullets.remove(bullet)


# Controls
p1_controls = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "shoot": pygame.K_SPACE,
    "facing": "right",
}
p2_controls = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "shoot": pygame.K_RETURN,
    "facing": "left",
}

player1 = Player(100, HEIGHT // 2, player1_img, p1_controls)
player2 = Player(WIDTH - 150, HEIGHT // 2, player2_img, p2_controls)

font = pygame.font.SysFont(None, 36)


def draw_health():
    h1 = font.render(f"P1 Health: {player1.health}", True, WHITE)
    h2 = font.render(f"P2 Health: {player2.health}", True, WHITE)
    screen.blit(h1, (10, 10))
    screen.blit(h2, (WIDTH - h2.get_width() - 10, 10))


def game_over(winner):
    screen.fill(BLACK)
    msg = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(
        msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2)
    )
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


# Main loop
while True:
    clock.tick(60)
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    current_time = pygame.time.get_ticks()
    if not shield_active and current_time - shield_spawn_time >= shield_spawn_delay:
        shield_rect.topleft = (
            random.randint(50, WIDTH - SHIELD_SIZE - 50),
            random.randint(50, HEIGHT - SHIELD_SIZE - 50),
        )
        shield_active = True

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == player1.controls["shoot"]:
                player1.shoot()
            if event.key == player2.controls["shoot"]:
                player2.shoot()

    # Update
    player1.move(keys)
    player2.move(keys)
    player1.update_bullets(player2)
    player2.update_bullets(player1)

    # Check if player picks up shield
    for player in [player1, player2]:
        if shield_active and player.rect.colliderect(shield_rect):
            player.shielded = True
            player.shield_start_time = current_time
            shield_active = False
            shield_spawn_time = current_time

    for player in [player1, player2]:
        if (
            player.shielded
            and current_time - player.shield_start_time >= shield_duration
        ):
            player.shielded = False

    # Draw
    for wall in walls:
        pygame.draw.rect(screen, (100, 100, 100), wall)

    player1.draw()
    player2.draw()
    if shield_active:
        pygame.draw.rect(screen, shield_color, shield_rect)

    draw_health()

    # Win condition
    if player1.health <= 0:
        game_over("Player 2")
    elif player2.health <= 0:
        game_over("Player 1")

    pygame.display.flip()
