import pygame

# Initialize pygame
pygame.init()

# Set display dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Display Image in Pygame")

# Load the image
image = pygame.image.load(r"C:\Users\Naman Patel\Desktop\Python_Progs\zombie.png")  # Replace with your image file path
image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the image

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (optional)
    screen.fill((30, 30, 30))

    # Draw the image
    screen.blit(image, image_rect)

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
