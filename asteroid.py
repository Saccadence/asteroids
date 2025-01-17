import pygame
import random
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def  __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return
        random_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        if new_radius < ASTEROID_MIN_RADIUS:
            new_radius =  ASTEROID_MIN_RADIUS
        
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_1.velocity = self.velocity.rotate(random_angle) * 1.2
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2.velocity = self.velocity.rotate(-random_angle) * 1.2
        
        self.kill()        
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt
        
        # Wrap around the screen horizontally and vertically
        if self.position.x < 0 - self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = 0 - self.radius

        if self.position.y < 0 - self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = 0 - self.radius