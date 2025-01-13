import pygame       # Pygame library (source venv/bin/activate)
import constants    # Constants.py library
from constants import *



   
def main():
    print("Starting asteroids!")
    pygame.init     # Start pygame
    
    # Delta Time - Frame Limiter
    clock = pygame.time.Clock()
    dt = 0
    
    # Define 'screen' (process window size) 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Game Loop
    while True:
        
        # Terminate process (QUIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((0, 0, 0))  # Fill screen with black
        pygame.display.flip()   # Refresh screen
        
        # Establish Frame Limit
        # Store time since last called (in seconds)
        dt = clock.tick(60) / 1000


    

if __name__ == "__main__":
    main()