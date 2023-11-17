import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blit Contents Under Pie-Shaped Mask")
clock = pygame.time.Clock()

# Create a target surface
target_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Create a pie-shaped mask
mask_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.pie(mask_surface, WHITE, (WIDTH // 2, HEIGHT // 2, 100, 45, 135))  # Parameters: surface, color, rect, start_angle, stop_angle

# Convert the mask to a mask object
mask = pygame.mask.from_surface(mask_surface)

# Create contents to be blitted under the pie-shaped mask
contents_surface = pygame.Surface((WIDTH, HEIGHT))
contents_surface.fill(RED)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    target_surface.fill(BLACK)

    # Blit the contents surface under the pie-shaped mask
    target_surface.blit(contents_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT, area=mask)

    # Update the display
    screen.blit(target_surface, (0, 0))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()