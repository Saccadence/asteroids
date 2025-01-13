import pygame       # Pygame library (source venv/bin/activate)
import constants    # Constants.py library
from constants import *


def main():
    print("Starting asteroids!")
    pygame.init     # Start pygame
    
    # Define 'screen' (process window size) 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Game Loop
    while True:
        screen.fill((0, 0, 0))  # Fill screen with black
        pygame.display.flip()   # Refresh screen


    

if __name__ == "__main__":
    main()