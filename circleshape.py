import pygame


class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        
    def draw(self, screen):
        pass        # Subclasses will override
    
    def update(self, dt):
        pass        # Subclasses will override
    
    def detect_collision(self, other):
        if (self.radius + other.radius) >= self.position.distance_to(other.position):
            return True
        return False