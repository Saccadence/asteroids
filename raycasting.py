import pygame
from circleshape import CircleShape
from constants import *

class Raycasting(CircleShape):
    def __init__(self, position, vector):
        super().__init__(position.x, position.y, 0)
        self.vector = pygame.Vector2(vector)
        self.decay = vector.length()
