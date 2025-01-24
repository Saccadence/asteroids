import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.momentum = 0
        self.accel_time = 0
        self.decel_time = 0
        self.inertia = 0
        self.speed = 0
        self.shot_time = 0
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
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.speed = self.momentum * PLAYER_SPEED
        self.position += forward * self.speed * dt
        print(f"Momentum = {self.momentum} | Accel = {self.accel_time} | Decel = {self.decel_time}\nSpeed = {self.speed}")
        
    def accelerate(self, dt):
        # Acceleration
        if self.keys[pygame.K_w] or self.keys[pygame.K_s]:
            if self.accel_time > 0 or self.accel_time < PLAYER_ACCELERATE:
                self.accel_time += dt
            if self.decel_time > 0 or self.decel_time < PLAYER_DECELERATE:
                self.decel_time -= dt
        # Speed Decay
        else:
            if self.accel_time > 0 or self.accel_time < PLAYER_ACCELERATE:
                self.accel_time -= dt
            if self.decel_time > 0 or self.decel_time < PLAYER_DECELERATE:
                self.decel_time += dt
        self.accel_time = self.check_limit(self.accel_time, PLAYER_ACCELERATE)
        self.decel_time = self.check_limit(self.decel_time, PLAYER_DECELERATE)
        # Momentum as difference of percentage accel - percentage decel
        self.momentum = abs((self.accel_time / PLAYER_ACCELERATE) - (self.decel_time / PLAYER_DECELERATE))
            
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
        self.inertia = self.position + pygame.Vector2(0, 1).rotate(self.rotation) * self.speed
        self.accelerate(dt)
        
        if self.keys[pygame.K_w]:
            self.move(dt)
        if self.keys[pygame.K_s]:
            self.move(-dt)
        if self.keys[pygame.K_d]:
            self.rotate(dt)
        if self.keys[pygame.K_a]:
            self.rotate(-dt)
        if self.keys[pygame.K_SPACE]:
            self.shoot()