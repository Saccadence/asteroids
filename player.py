import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.momentum = 0
        self.move_time = 0
        self.speed = 0
        self.shot_time = 0
    
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
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * self.momentum * dt
        
    def inertia(self, dt):
        if self.keys[pygame.K_w] or self.keys[pygame.K_s]:
            self.move_time += dt
        else:
            self.move_time -= dt
            if abs(self.move_time) <= 0 + abs(dt):
                self.move_time = 0
                self.momentum = 0
        if abs(self.move_time) >= PLAYER_ACCELERATE:
            if self.move_time < 0:
                self.move_time = -PLAYER_ACCELERATE
            else:
                self.move_time = PLAYER_ACCELERATE

        self.momentum = self.move_time / PLAYER_ACCELERATE 
        print(self.momentum)
        
    def shoot(self):
        if self.shot_time <= 0:
            self.shot_time = PLAYER_SHOOT_COOLDOWN
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            nose_position = self.position + forward * self.radius
            shot = Shot(nose_position.x, nose_position.y)
            shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def update(self, dt):
        self.shot_time -= dt
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
        if not self.keys[pygame.K_w] or self.keys[pygame.K_s]:
            self.inertia(dt)