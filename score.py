import pygame
from constants import *



class KillScore(pygame.sprite.Sprite):
    def __init__(self, asteroid, kill_font):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.kill_scored = asteroid.radius * SCORE_GAIN
        self.kill_score_time = SCORE_TIME
        self.kill_text_position = (asteroid.position.x, asteroid.position.y)
        self.kill_font = kill_font
        self.alpha = 255
    
    def update(self, dt):
        self.kill_score_time -= dt
        self.alpha -= (dt * 255) / SCORE_TIME
        if self.alpha < 0:
            self.alpha = 0
    
    def draw(self, screen):
        kill_text_surface = self.kill_font.render(f"{self.kill_scored}", True, (255, 255, 255))
        kill_text_surface.set_alpha(self.alpha)
        screen.blit(kill_text_surface, self.kill_text_position)
