import pygame

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Simple Game")

# Player properties
player_size = 50
player_x = (screen_width - player_size) // 2
player_y = screen_height - player_size - 10
player_color = (255, 0, 0) # Red

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle keyboard input for player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= 10
            if event.key == pygame.K_RIGHT:
                player_x += 10

    # Fill the background with a color (e.g., blue)
    screen.fill((0, 0, 255))

    # Draw the player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
