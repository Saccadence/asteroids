import pygame       # Pygame library (source venv/bin/activate)
from constants import *
from player import Player



def main():
    print("Starting asteroids!")
    pygame.init     # Start pygame
    
    # Define Objects and Variables
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    
    # Game Loop
    while True:
        
        # Terminate process (QUIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # Render Methods
        screen.fill((0, 0, 0))  # Fill screen with black
        player.draw(screen)
        pygame.display.flip()   # Refresh screen
        
        # Establish (60 FPS) Frame Limit
        dt = clock.tick(60) / 1000  # Store time since last called (in seconds)



if __name__ == "__main__":
    main()