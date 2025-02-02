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
        self.mass = radius ** 2
        self.bounced = False
        
    def draw(self, screen):
        pass        # Subclasses will override
    
    def update(self, dt):
        pass        # Subclasses will override
    
    def detect_collision(self, other):
        return self.position.distance_to(other.position) < (self.radius + other.radius)

    def check_limit(self, input, limit):
        try:
            if input > 0 and input < limit:
                return input
            elif input >= limit:
                return limit
            elif input <= 0:
                return 0
        except:
            raise Exception("check_limit broke")

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
        v1n_final = (v1n * (self.mass - other.mass) + 2 * other.mass * v2n) / (self.mass + other.mass)
        v2n_final = (v2n * (other.mass - self.mass) + 2 * self.mass * v1n) / (self.mass + other.mass)

        # Convert scalar normal and tangential velocities back to vectors
        self.velocity = v1n_final * normal + v1t * tangent
        other.velocity = v2n_final * normal + v2t * tangent
        
        self.bounced = True
        other.bounced = True