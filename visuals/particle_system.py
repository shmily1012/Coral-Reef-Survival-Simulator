import pygame
import random
import math
import config

class Particle:
    def __init__(self, x, y, color, velocity=(0, 0), lifetime=1.0, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.time_remaining = lifetime
        self.size = size
        self.alpha = 255
        
    def update(self, delta_time):
        self.x += self.velocity[0] * delta_time
        self.y += self.velocity[1] * delta_time
        self.time_remaining -= delta_time
        self.alpha = int(255 * (self.time_remaining / self.lifetime))
        return self.time_remaining <= 0
        
    def draw(self, screen):
        if self.alpha > 0:
            surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, self.alpha), (self.size, self.size), self.size)
            screen.blit(surface, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    """
    A system for managing and rendering particle effects.
    
    This class handles creation, updating and drawing of particle effects like bubbles
    and warning indicators. It maintains a list of active particles and automatically
    removes them when their lifetime expires.
    
    Attributes:
        screen: The pygame surface to draw particles on
        particles: List of active Particle objects
    """
    
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        
    def create_bubble_effect(self, x, y, count=5):
        for _ in range(count):
            velocity = (random.uniform(-20, 20), random.uniform(-50, -20))
            self.particles.append(
                Particle(x, y, (255, 255, 255), velocity, 
                        random.uniform(0.5, 1.5), random.randint(2, 4))
            )
            
    def create_warning_effect(self, x, y, count=20):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 100)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            self.particles.append(
                Particle(x, y, (255, 50, 50), velocity, 
                        random.uniform(0.5, 1.0), random.randint(2, 4))
            )
    
    def update(self, delta_time):
        self.particles = [p for p in self.particles if not p.update(delta_time)]
        
    def draw(self):
        for particle in self.particles:
            particle.draw(self.screen) 