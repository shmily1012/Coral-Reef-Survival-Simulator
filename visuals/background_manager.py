import pygame
import config
from visuals.animations import CoralAnimation, FishAnimation

class BackgroundManager:
    def __init__(self, screen):
        self.screen = screen
        self.corals = []
        self.fishes = []
        self.health_state = "healthy"  # States: healthy, stressed, bleached
        
        # Initialize coral positions
        coral_positions = [
            (100, 600), (300, 650), (500, 620),
            (700, 640), (900, 610), (200, 630)
        ]
        
        # Create coral animations
        for pos in coral_positions:
            self.corals.append(CoralAnimation(pos[0], pos[1]))
            
        # Create fish schools
        for _ in range(3):  # 3 schools of fish
            self.fishes.append(FishAnimation(self.screen))
            
    def update(self, delta_time, health):
        # Update health state
        if health > 70:
            self.health_state = "healthy"
        elif health > 30:
            self.health_state = "stressed"
        else:
            self.health_state = "bleached"
            
        # Update animations
        for coral in self.corals:
            coral.update(delta_time, self.health_state)
            
        for fish in self.fishes:
            fish.update(delta_time, self.health_state)
            
    def draw(self):
        # Draw water gradient background
        self.draw_water_gradient()
        
        # Draw corals
        for coral in self.corals:
            coral.draw(self.screen)
            
        # Draw fish
        for fish in self.fishes:
            fish.draw(self.screen)
            
    def draw_water_gradient(self):
        height = config.SCREEN_HEIGHT
        for y in range(0, height, 2):
            # Create gradient from light to dark blue
            color_value = int(255 * (1 - y/height))
            color = (0, color_value, min(255, color_value + 100))
            pygame.draw.line(self.screen, color, (0, y), (config.SCREEN_WIDTH, y)) 