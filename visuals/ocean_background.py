import pygame
import math
import numpy as np
from pygame import Surface
import config

class OceanBackground:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.time = 0
        self.wave_offset = 0
        self.wave_speed = 2
        self.wave_amplitude = 15
        self.wave_frequency = 0.02
        
        # Create gradient colors for the ocean
        self.colors = [
            (0, 85, 128),    # Deeper blue
            (0, 105, 148),   # Middle blue
            (0, 125, 168)    # Lighter blue
        ]
        
        # Create surface for the waves
        self.wave_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.num_waves = 5
        
    def update(self, delta_time: float):
        self.time += delta_time
        self.wave_offset = (self.wave_offset + self.wave_speed * delta_time) % config.SCREEN_WIDTH
        
    def draw(self):
        # Fill with base color
        self.wave_surface.fill(self.colors[0])
        
        # Draw multiple wave layers
        for i in range(self.num_waves):
            wave_points = []
            phase_offset = i * math.pi / 4
            amplitude = self.wave_amplitude * (1 - i * 0.15)
            frequency = self.wave_frequency * (1 + i * 0.1)
            
            # Calculate wave points
            for x in range(0, config.SCREEN_WIDTH + 2, 2):
                y_base = 150 + i * 100  # Vertical spacing between waves
                y = y_base + amplitude * math.sin(
                    (x + self.wave_offset) * frequency + self.time + phase_offset
                )
                wave_points.append((x, y))
            
            # Draw wave
            if len(wave_points) > 1:
                # Create filled wave
                points = wave_points + [(config.SCREEN_WIDTH, config.SCREEN_HEIGHT), 
                                      (0, config.SCREEN_HEIGHT)]
                pygame.draw.polygon(self.wave_surface, self.colors[min(i + 1, 2)], points)
        
        # Apply some alpha blending for smoother appearance
        self.wave_surface.set_alpha(230)
        self.screen.blit(self.wave_surface, (0, 0)) 