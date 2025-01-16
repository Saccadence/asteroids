import sys
import pygame       # Pygame library (source venv/bin/activate)
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import KillScore



def main():
    print("Starting asteroids!")
    pygame.init     # Start pygame
    pygame.font.init()

    # Define Objects and Variables
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    score_font = pygame.font.Font("Silkscreen-Regular.ttf", 36)
    kill_font = pygame.font.Font("Silkscreen-Regular.ttf", 16)

    # Define groups to be called
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    kill_scores = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    KillScore.containers = (kill_scores, updatable, drawable)
    asteroid_field = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    big_one = 0
    big_one_time = random.randint(15, 45)

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
        for asteroid in asteroids:
            if asteroid.detect_collision(player):
                print("Game over!")
                sys.exit()
            for shot in shots:
                if asteroid.detect_collision(shot):
                    shot.kill()
                    kill_score = KillScore(asteroid, kill_font)
                    score +=  asteroid.radius * SCORE_GAIN
                    asteroid.split()
        for kill_score in kill_scores:
            if kill_score.kill_score_time <= 0:
                kill_score.kill()
        if big_one >= big_one_time:
            asteroid
        

        # Render
        screen.fill((0, 0, 0))  # Fill screen with black
        for obj in drawable:
            obj.draw(screen)
        score_text = score_font.render(f"{score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))           # Render TOTAL score over everything
        if dt > 0:
            fps = int(1 // dt)
            screen.blit(score_font.render(f"{fps}", True, (255, 255, 255)), ((SCREEN_WIDTH - 90), 10))   # FPS Counter
        else:
            screen.blit(score_font.render(f"999", True, (255, 255, 255)), (10, (SCREEN_WIDTH - SCREEN_WIDTH / 20)))
        
        pygame.display.flip()   # Refresh screen

        # Establish (240 FPS) Frame Limit
        dt = clock.tick(240) / 1000  # Store time since last called (in seconds)


if __name__ == "__main__":
    main()
