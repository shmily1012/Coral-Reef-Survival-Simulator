import pygame
import random
import math
import config
import os

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
        
        # Load fish images
        self.fish_images = self.load_fish_images()
        
        # Create fish instances with random images and positions
        self.fishes = []
        for _ in range(self.fish_count):
            self.fishes.append({
                'offset': (random.uniform(-20, 20), random.uniform(-10, 10)),
                'image': random.choice(self.fish_images),
                'scale': random.uniform(0.8, 1.2)  # Random size variation
            })
            
    def load_fish_images(self):
        images = []
        fish_folder = os.path.join("assets", "images", "fish")
        reduced_size_by_percent = 0.1
        try:
            for filename in os.listdir(fish_folder):
                if filename.endswith(('.png', '.jpg')):
                    image_path = os.path.join(fish_folder, filename)
                    image = pygame.image.load(image_path).convert_alpha()
                    # Scale image to 30% of original size
                    new_width = int(image.get_width() * reduced_size_by_percent)
                    new_height = int(image.get_height() * reduced_size_by_percent)
                    image = pygame.transform.scale(image, (new_width, new_height))
                    images.append(image)
        except:
            print("Warning: Could not load fish images")
            # Create a default colored rectangle as fallback
            fallback = pygame.Surface((40, 30))
            fallback.fill((255, 165, 0))
            images.append(fallback)
        return images
        
    def update(self, delta_time, health_state):
        # Move fish school in opposite direction
        self.x -= self.speed * delta_time * self.direction
        
        # Wrap around screen (reversed logic)
        if self.direction > 0 and self.x < -50:
            self.x = config.SCREEN_WIDTH + 50
        elif self.direction < 0 and self.x > config.SCREEN_WIDTH + 50:
            self.x = -50
            
        # Adjust behavior based on reef health
        if health_state == "stressed":
            self.speed = random.uniform(70, 120)
        elif health_state == "bleached":
            self.speed = random.uniform(100, 150)
    def draw(self, screen):
        for fish in self.fishes:
            fish_x = self.x + fish['offset'][0]
            fish_y = self.y + fish['offset'][1]
            
            # Get the fish image and scale it
            image = fish['image']
            scaled_size = (
                int(image.get_width() * fish['scale']),
                int(image.get_height() * fish['scale'])
            )
            scaled_image = pygame.transform.scale(image, scaled_size)
            
            # Flip image if moving left
            if self.direction < 0:
                scaled_image = pygame.transform.flip(scaled_image, True, False)
                
            # Draw the fish
            screen.blit(scaled_image, (fish_x - scaled_size[0]/2, fish_y - scaled_size[1]/2)) 