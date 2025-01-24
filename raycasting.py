import pygame
from circleshape import CircleShape
from constants import *

class Raycasting(CircleShape):
    def __init__(self, position, vector):
        super().__init__(self, position.x, position.y, 0)
        self.vector = vector
        self.decay = PLAYER_RADIUS
        
    def update(self, dt):
        self.decay -= self.decay / dt
        self.vector = self.decay - (self.vector / self.decay)
