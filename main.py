import sys
import os
import pygame       # Pygame library (source venv/bin/activate)
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
                    kill_score = KillScore(asteroid)
                    asteroid.split()
        for score in kill_scores:
            if score.kill_score_time:
                return

        # Render
        screen.fill((0, 0, 0))  # Fill screen with black

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()   # Refresh screen

        # Establish (120 FPS) Frame Limit
        dt = clock.tick(120) / 1000  # Store time since last called (in seconds)


if __name__ == "__main__":
    main()
