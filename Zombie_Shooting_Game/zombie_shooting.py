import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player settings
gun_angle = 0
player_size = 100
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 8

# Load player image
try:
    player_img_original = pygame.image.load("gun_imagee.jpg").convert_alpha()
except:
    print("Error: gun_imagee.jpg not found")
    sys.exit()

player_img_original = pygame.transform.scale(player_img_original, (player_size, player_size))

# Bullet settings
bullet_width = 5
bullet_height = 15
bullet_speed = 10
try:
    shoot_sound = pygame.mixer.Sound("gun_sound.mp3")
    blast_sound = pygame.mixer.Sound("gun_blast.wav")
except:
    print("Error: Sound files not found")
    sys.exit()

bullets = []
bullet_cooldown = 10
bullet_timer = 0

# Zombie settings
zombie_size = 75
zombie_speed = 1
zombies = []
try:
    zombie_img = pygame.image.load("zombie.png").convert_alpha()
except:
    print("Error: zombie.png not found")
    sys.exit()

zombie_img = pygame.transform.scale(zombie_img, (zombie_size, zombie_size))

spawn_delay = 69
frame_count = 0

# Score
score = 0
font = pygame.font.Font(None, 36)

# Clock and game state
clock = pygame.time.Clock()
running = True

def draw_rotated_player():
    rotated_image = pygame.transform.rotate(player_img_original, gun_angle)
    new_rect = rotated_image.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
    screen.blit(rotated_image, new_rect.topleft)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], bullet_width, bullet_height))

def draw_zombies():
    for zombie in zombies:
        screen.blit(zombie_img, (zombie[0], zombie[1]))

def handle_collisions():
    global score
    for bullet in bullets[:]:
        for zombie in zombies[:]:
            if (
                bullet["x"] < zombie[0] + zombie_size and
                bullet["x"] + bullet_width > zombie[0] and
                bullet["y"] < zombie[1] + zombie_size and
                bullet["y"] + bullet_height > zombie[1]
            ):
                if bullet in bullets:
                    bullets.remove(bullet)
                if zombie in zombies:
                    zombies.remove(zombie)
                blast_sound.play()
                score += 1

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Main game loop
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()

    # Rotate gun
    if keys[pygame.K_LEFT]:
        gun_angle += 2
    if keys[pygame.K_RIGHT]:
        gun_angle -= 2
    gun_angle %= 360

    # Shoot bullet
    if keys[pygame.K_SPACE] and bullet_timer == 0:
        rad_angle = math.radians(gun_angle)
        vx = bullet_speed * math.cos(rad_angle)
        vy = -bullet_speed * math.sin(rad_angle)
        bullet = {
            "x": player_x + player_size // 2,
            "y": player_y + player_size // 2,
            "vx": vx,
            "vy": vy
        }
        bullets.append(bullet)
        shoot_sound.play()
        bullet_timer = bullet_cooldown

    if bullet_timer > 0:
        bullet_timer -= 1

    # Move bullets
    new_bullets = []
    for bullet in bullets:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]
        if 0 <= bullet["x"] <= WIDTH and 0 <= bullet["y"] <= HEIGHT:
            new_bullets.append(bullet)
    bullets = new_bullets

    # Spawn zombies
    frame_count += 1
    if frame_count >= spawn_delay:
        zombies.append([random.randint(0, WIDTH - zombie_size), -zombie_size])
        frame_count = 0

    # Move zombies
    zombies = [[x, y + zombie_speed] for x, y in zombies]

    # Collision detection
    handle_collisions()

    # Draw everything
    draw_rotated_player()
    draw_bullets()
    draw_zombies()
    draw_score()

    # Game over condition
    for zombie in zombies:
        if zombie[1] + zombie_size >= HEIGHT:
            print(f"Game Over! Final Score: {score}")
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

