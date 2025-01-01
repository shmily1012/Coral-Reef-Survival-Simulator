import pygame
import config
from visuals.animations import CoralAnimation, FishAnimation
import random

class BackgroundManager:
    def __init__(self, screen):
        self.screen = screen
        self.corals = []
        self.bubbles = []
        self.health_state = 100  # Initialize with full health
        
        # Add water current particles
        self.water_particles = []
        for _ in range(50):  # Create 50 water current particles
            self.water_particles.append({
                'x': random.randint(0, config.SCREEN_WIDTH),
                'y': random.randint(0, config.SCREEN_HEIGHT),
                'speed': random.uniform(10, 30),
                'alpha': random.randint(20, 60)  # Transparency
            })
        
        # Create background corals
        for _ in range(5):
            x = random.randint(0, config.SCREEN_WIDTH)
            y = random.randint(config.SCREEN_HEIGHT - 100, config.SCREEN_HEIGHT)
            self.corals.append(CoralAnimation(x, y))
            
        # Create initial bubbles
        self.create_bubbles()
        
    def update(self, delta_time, health_value):
        """
        Update background elements.
        
        Args:
            delta_time (float): Time since last update
            health_value (float): Current health value (0-100)
        """
        # Convert health_value to float if it's a string
        if isinstance(health_value, str):
            try:
                health_value = float(health_value)
            except ValueError:
                health_value = 100  # Default to full health if conversion fails
        
        self.health_state = health_value
        
        # Update water current particles
        for particle in self.water_particles:
            particle['x'] += particle['speed'] * delta_time
            if particle['x'] > config.SCREEN_WIDTH:
                particle['x'] = -5
                particle['y'] = random.randint(0, config.SCREEN_HEIGHT)
        
        # Update background corals
        for coral in self.corals:
            coral.update(delta_time, self.health_state)
            
        # Update bubbles
        self.update_bubbles(delta_time)
        
        # Create new bubbles occasionally
        if random.random() < delta_time * 0.5:
            self.create_bubbles()
            
    def create_bubbles(self):
        """Create new bubble particles."""
        for _ in range(random.randint(1, 3)):
            x = random.randint(0, config.SCREEN_WIDTH)
            y = config.SCREEN_HEIGHT + 10
            size = random.randint(2, 6)
            speed = random.uniform(30, 50)
            self.bubbles.append({
                'x': x,
                'y': y,
                'size': size,
                'speed': speed
            })
            
    def update_bubbles(self, delta_time):
        """Update bubble positions and remove off-screen bubbles."""
        new_bubbles = []
        for bubble in self.bubbles:
            bubble['y'] -= bubble['speed'] * delta_time
            if bubble['y'] > -10:  # Keep bubble if still on screen
                new_bubbles.append(bubble)
        self.bubbles = new_bubbles
        
    def draw(self):
        """Draw all background elements."""
        # Draw water current particles first
        water_surface = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        for particle in self.water_particles:
            pygame.draw.circle(
                water_surface,
                (255, 255, 255, particle['alpha']),
                (int(particle['x']), int(particle['y'])),
                1
            )
        self.screen.blit(water_surface, (0, 0))
        
        # Draw the rest of the elements
        for coral in self.corals:
            coral.draw(self.screen)
            
        for bubble in self.bubbles:
            pygame.draw.circle(
                self.screen,
                (255, 255, 255, 128),
                (int(bubble['x']), int(bubble['y'])),
                bubble['size']
            ) 