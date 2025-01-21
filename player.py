import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.momentum = 0
        self.timer = 0
    
    def triangle(self):
        # Define coordinates for points on triangle *relative* to center
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        
        # Calculate and return said *absolute* coordinates
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def move(self, dt):
        if not self.keys[pygame.K_w] or self.keys[pygame.K_s]:
            if not self.momentum == PLAYER_DECELERATE:
                self.momentum = PLAYER_DECELERATE
            self.momentum -= dt
        else:
            self.momentum = PLAYER_ACCELERATE
            self.momentum += dt
        forward = pygame.Vector2(0, 1).rotate(self.rotation) * self.momentum
        self.position += forward * PLAYER_SPEED * dt
        
    def shoot(self):
        if self.timer <= 0:
            self.timer = PLAYER_SHOOT_COOLDOWN
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            nose_position = self.position + forward * self.radius
            shot = Shot(nose_position.x, nose_position.y)
            shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def update(self, dt):
        self.timer -= dt
        self.keys = pygame.key.get_pressed()
        
        if self.keys[pygame.K_w]:
            self.move(dt)
        if self.keys[pygame.K_a]:
            self.rotate(-dt)
        if self.keys[pygame.K_s]:
            self.move(-dt)
        if self.keys[pygame.K_d]:
            self.rotate(dt)
        if self.keys[pygame.K_SPACE]:
            self.shoot()