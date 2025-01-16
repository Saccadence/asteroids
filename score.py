import pygame
from constants import *



class KillScore():
    def __init__(self, asteroid):
        self.score = 0
        self.kill_score = 0
        self.kill_score_time = 0
        self.kill_text_position = (asteroid.position.x, asteroid.position.y)
        self.score_font = pygame.font.Font("Silkscreen-Regular.ttf", 36)
        self.kill_font = pygame.font.Font("Silkscreen-Regular.ttf", 12)
        
    
    def draw(self, screen):
        score_text = self.score_font.render(f"{self.score}", True, (255, 255, 255))
        kill_text = self.kill_font.render(f"{self.kill_score}", True, (255, 255, 255))
        screen.blit(kill_text, self.kill_text_position)
        screen.blit(score_text, (10, 10))
    
    def update(self, asteroid, dt):
        self.kill_score = asteroid.radius * SCORE_GAIN
        self.kill_score_time += dt
        self.score += self.kill_score
        
        