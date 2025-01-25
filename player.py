import pygame
import sys
from constants import *
from circleshape import CircleShape
from shot import Shot
from raycasting import Raycasting


class Player(CircleShape):
    
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.rotation_accel = 0
        self.velocity = pygame.Vector2(0, 0)
        self.angular_velocity = 0
        self.shot_time = 0
        self.timer = 0
        self.rays = pygame.sprite.Group()
        Raycasting.containers = self.rays
    
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
        for ray in self.rays:
            pygame.draw.line(screen, (255, 0, 0), self.position, self.position + ray.vector, 2)

        
    def rotate(self, dt, direction):
        if abs(self.rotation_accel) < PLAYER_MAX_ROTATION_ACCEL:
            self.rotation_accel += direction * PLAYER_ROTATION_INCREMENT * dt
        else:
            self.rotation_accel = max(min(self.rotation_accel, PLAYER_MAX_ROTATION_ACCEL), -PLAYER_MAX_ROTATION_ACCEL)
        self.rotation += self.rotation_accel * dt
        self.rotation %= 360
        self.angular_velocity = self.rotation_accel * dt

    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        backward = -forward
        # Apply thrust when pressing the W key (forward thrust)
        if self.keys[pygame.K_w]:
            if self.velocity.length() < PLAYER_MAX_SPEED:
                self.velocity += forward * PLAYER_THRUST * dt  # Accelerate forward
            else:
                self.velocity.scale_to_length(PLAYER_MAX_SPEED)  # Cap forward speed
        # Apply reverse thrust when pressing the S key (backward thrust)
        if self.keys[pygame.K_s]:
            if self.velocity.length() > -PLAYER_MAX_REVERSE_SPEED:
                self.velocity += backward * PLAYER_THRUST * dt  # Accelerate backward (reverse)
            else:
                self.velocity.scale_to_length(-PLAYER_MAX_REVERSE_SPEED)  # Cap reverse speed
    
    def apply_drag(self, dt):
        # Apply some form of drag to reduce velocity when no keys are pressed
        if not self.keys[pygame.K_w] and not self.keys[pygame.K_s]:
            self.velocity *= (1 - PLAYER_DRAG * dt)  # Slow down gradually
        # Limit the velocity to prevent it from going below zero (for reverse)
        if self.velocity.length() < 0.1:
            self.velocity = pygame.Vector2(0, 0)  # Stop when the velocity is very small

            
    def shoot(self):
        if self.shot_time <= 0:
            self.shot_time = PLAYER_SHOOT_COOLDOWN
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            nose_position = self.position + forward * self.radius
            shot = Shot(nose_position.x, nose_position.y)
            shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def update(self, dt):
        direction = 0
        self.timer += dt
        self.shot_time -= dt
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_SPACE]:
            self.shoot()
            
        if self.keys[pygame.K_d]:
            self.rotate(dt, 1)
        if self.keys[pygame.K_a]:
            self.rotate(-dt, -1)
            
        self.accelerate(dt)
        self.apply_drag(dt)
        
        if self.timer > 0.01:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            ray_magnitude = self.velocity.magnitude()
            new_ray = Raycasting(self.position, forward * ray_magnitude)
            self.rays.add(new_ray)
            self.timer = 0
        
        total_ray_vector = pygame.Vector2(0, 0)
        ray_count = 0
        for ray in self.rays:
            self.position += ray.vector * dt
            ray.decay -= dt * RAY_DECAY_RATE  # Decrease ray magnitude
            if ray.vector.length() > 0.001:
                ray.vector.scale_to_length(max(ray.decay, 0))  # Scale vector length to decay value
                total_ray_vector += ray.vector
                ray_count += 1
            else:
                ray.vector = pygame.Vector2(0,0)
            if ray.decay <= 0:
                ray.kill()  # Remove expired rays
        
        if ray_count > 0:
            average_ray_vector = total_ray_vector / ray_count
            self.velocity += average_ray_vector * RAY_VELOCITY_FACTOR * dt  # Control ray impact
        
        self.position += self.velocity * dt
        
        # Screen wrapping
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
