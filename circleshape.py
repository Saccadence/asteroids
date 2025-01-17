import pygame
import math


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.bounced = False
        
    def draw(self, screen):
        pass        # Subclasses will override
    
    def update(self, dt):
        pass        # Subclasses will override
    
    def detect_collision(self, other):
        return self.position.distance_to(other.position) < (self.radius + other.radius)

    def bounce_off(self, other):        
        # Normal vector
        normal = (self.position - other.position).normalize()
        tangent = pygame.Vector2(-normal.y, normal.x)

        # Decompose velocities into normal and tangential components
        v1n = self.velocity.dot(normal)
        v1t = self.velocity.dot(tangent)
        v2n = other.velocity.dot(normal)
        v2t = other.velocity.dot(tangent)

        # Elastic collision formula for normal components
        v1n_final = (v1n * (self.radius - other.radius) + 2 * other.radius * v2n) / (self.radius + other.radius)
        v2n_final = (v2n * (other.radius - self.radius) + 2 * self.radius * v1n) / (self.radius + other.radius)

        # Convert scalar normal and tangential velocities back to vectors
        self.velocity = v1n_final * normal + v1t * tangent
        other.velocity = v2n_final * normal + v2t * tangent
        
        self.bounced = True
        other.bounced = True