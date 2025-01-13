import pygame       # Pygame library (source venv/bin/activate)
from constants import *
from player import Player



def main():
    print("Starting asteroids!")
    pygame.init     # Start pygame
    
    # Define Objects and Variables
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Define groups to be called
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    dt = 0
    
    # Game Loop
    while True:
        
        # Terminate process (QUIT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        
        # Update
        for obj in updatable:
            obj.update(dt)
        
        # Render
        screen.fill((0, 0, 0))  # Fill screen with black
        
        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()   # Refresh screen
        
        # Establish (60 FPS) Frame Limit
        dt = clock.tick(60) / 1000  # Store time since last called (in seconds)



if __name__ == "__main__":
    main()