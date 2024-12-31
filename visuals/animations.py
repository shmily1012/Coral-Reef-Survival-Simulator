import pygame
import random
import math
import config

class CoralAnimation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sway_offset = random.random() * math.pi * 2
        self.sway_speed = 1.0
        self.time = 0
        self.color = config.WHITE
        self.size = random.randint(40, 60)
        self.branches = self._generate_branches()
        
    def _generate_branches(self):
        branches = []
        num_branches = random.randint(3, 6)
        for _ in range(num_branches):
            angle = random.uniform(-math.pi/3, math.pi/3)
            length = random.uniform(0.5, 1.0) * self.size
            branches.append((angle, length))
        return branches
        
    def update(self, delta_time, health_state):
        self.time += delta_time * self.sway_speed
        
        # Update coral color based on health
        if health_state == "healthy":
            self.color = (255, 127, 127)  # Pink
        elif health_state == "stressed":
            self.color = (255, 200, 127)  # Orange
        else:
            self.color = (255, 255, 255)  # White (bleached)
            
    def draw(self, screen):
        sway = math.sin(self.time + self.sway_offset) * 5
        
        # Draw each branch
        for angle, length in self.branches:
            end_x = self.x + math.cos(angle) * length + sway
            end_y = self.y - math.sin(angle) * length
            
            pygame.draw.line(screen, self.color, 
                           (self.x, self.y), (end_x, end_y), 3)
            
            # Draw polyps
            pygame.draw.circle(screen, self.color, (int(end_x), int(end_y)), 4)

class FishAnimation:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(0, config.SCREEN_WIDTH)
        self.y = random.randint(100, 400)
        self.speed = random.uniform(50, 100)
        self.direction = 1 if random.random() > 0.5 else -1
        self.fish_count = random.randint(5, 8)
        self.fish_offsets = [(random.uniform(-20, 20), random.uniform(-10, 10)) 
                            for _ in range(self.fish_count)]
        
    def update(self, delta_time, health_state):
        # Move fish school
        self.x += self.speed * delta_time * self.direction
        
        # Wrap around screen
        if self.direction > 0 and self.x > config.SCREEN_WIDTH + 50:
            self.x = -50
        elif self.direction < 0 and self.x < -50:
            self.x = config.SCREEN_WIDTH + 50
            
        # Adjust behavior based on reef health
        if health_state == "stressed":
            self.speed = random.uniform(70, 120)
        elif health_state == "bleached":
            self.speed = random.uniform(100, 150)
            
    def draw(self, screen):
        for offset_x, offset_y in self.fish_offsets:
            fish_x = self.x + offset_x
            fish_y = self.y + offset_y
            
            # Draw simple fish shape
            points = [
                (fish_x, fish_y),
                (fish_x - 15 * self.direction, fish_y - 8),
                (fish_x - 15 * self.direction, fish_y + 8)
            ]
            pygame.draw.polygon(screen, (255, 200, 0), points)  # Yellow fish
            
            # Draw tail
            tail_points = [
                (fish_x - 15 * self.direction, fish_y - 6),
                (fish_x - 25 * self.direction, fish_y),
                (fish_x - 15 * self.direction, fish_y + 6)
            ]
            pygame.draw.polygon(screen, (255, 200, 0), tail_points) 