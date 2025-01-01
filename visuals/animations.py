"""
Animations Module

Handles visual elements of the game including coral and fish animations.
Creates and manages dynamic visual elements that respond to game state.

Features:
- Coral animation with health state visualization
- Fish schooling behavior
- Dynamic color changes based on health
- Particle effects integration
- Support for both procedural and sprite-based animations
"""

import pygame
import random
import math
import config
import os
from pygame import Color, Surface
import colorsys

class CoralAnimation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sway_offset = random.random() * math.pi * 2
        self.sway_speed = 0.8
        self.time = 0
        self.size = random.randint(50, 80)
        self.coral_type = random.choice(['branching', 'fan', 'brain'])
        self.color_variation = random.uniform(-0.1, 0.1)
        
        # Load coral images
        self.coral_images = self.load_coral_images()
        self.current_image = random.choice(self.coral_images) if self.coral_images else None
        
        # Keep the existing branch and polyp system as fallback
        self.branches = self._generate_branches()
        self.polyps = self._generate_polyps()

    def load_coral_images(self):
        images = []
        coral_folder = os.path.join("assets", "images", "corals")
        try:
            for filename in os.listdir(coral_folder):
                if filename.endswith(('.png', '.svg')):
                    image_path = os.path.join(coral_folder, filename)
                    original_image = pygame.image.load(image_path).convert_alpha()
                    
                    # Scale image to match the desired size
                    aspect_ratio = original_image.get_width() / original_image.get_height()
                    new_height = self.size
                    new_width = int(new_height * aspect_ratio)
                    
                    scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
                    images.append(scaled_image)
        except Exception as e:
            print(f"Warning: Could not load coral images: {e}")
        return images

    def _generate_branches(self):
        branches = []
        if self.coral_type == 'branching':
            num_branches = random.randint(5, 8)
            for _ in range(num_branches):
                angle = random.uniform(-math.pi/3, math.pi/3)
                length = random.uniform(0.6, 1.0) * self.size
                thickness = random.uniform(2, 4)
                sub_branches = self._generate_sub_branches(length)
                branches.append({
                    'angle': angle,
                    'length': length,
                    'thickness': thickness,
                    'sub_branches': sub_branches
                })
        elif self.coral_type == 'fan':
            num_branches = random.randint(12, 16)
            spread = math.pi / 2
            for i in range(num_branches):
                angle = -spread/2 + (spread * i / (num_branches-1))
                length = random.uniform(0.8, 1.0) * self.size
                thickness = random.uniform(1, 3)
                branches.append({
                    'angle': angle,
                    'length': length,
                    'thickness': thickness,
                    'sub_branches': []
                })
        else:  # brain coral
            num_folds = random.randint(6, 10)
            for i in range(num_folds):
                angle = math.pi/2
                length = random.uniform(0.3, 0.5) * self.size
                thickness = random.uniform(4, 6)
                branches.append({
                    'angle': angle,
                    'length': length,
                    'thickness': thickness,
                    'sub_branches': []
                })
        return branches

    def _generate_sub_branches(self, parent_length):
        sub_branches = []
        if random.random() < 0.7:  # 70% chance of having sub-branches
            num_sub = random.randint(2, 4)
            for _ in range(num_sub):
                angle = random.uniform(-math.pi/4, math.pi/4)
                length = random.uniform(0.3, 0.6) * parent_length
                thickness = random.uniform(1, 2)
                sub_branches.append({
                    'angle': angle,
                    'length': length,
                    'thickness': thickness
                })
        return sub_branches

    def _generate_polyps(self):
        polyps = []
        num_polyps = random.randint(15, 25)
        for _ in range(num_polyps):
            offset_x = random.uniform(-self.size/2, self.size/2)
            offset_y = random.uniform(-self.size/2, 0)
            size = random.uniform(2, 4)
            polyps.append({
                'offset': (offset_x, offset_y),
                'size': size
            })
        return polyps

    def _get_health_color(self, health_value):
        """
        Get coral color based on numeric health value.
        
        Args:
            health_value (float): Health value from 0 to 100
        """
        # Determine health state based on value
        if health_value >= 70:
            health_state = 'healthy'
        elif health_value >= 30:
            health_state = 'stressed'
        else:
            health_state = 'bleached'
            
        base_colors = {
            'healthy': (255, 127, 127),  # Pink
            'stressed': (255, 200, 127),  # Orange
            'bleached': (255, 255, 255)   # White
        }
        
        base = Color(*base_colors[health_state])
        h, s, v, a = base.hsva  # Unpack all 4 components
        
        # Add slight color variation
        h = (h + self.color_variation * 20) % 360
        s = max(0, min(100, s + self.color_variation * 15))
        
        # Convert HSV to RGB (note: pygame's hsva uses 0-100 for s,v while colorsys uses 0-1)
        rgb = colorsys.hsv_to_rgb(h/360, s/100, v/100)
        
        # Scale RGB values to 0-255 range
        r = int(rgb[0] * 255)
        g = int(rgb[1] * 255)
        b = int(rgb[2] * 255)
        
        # Create color with RGB values
        return Color(r, g, b)

    def update(self, delta_time, health_value):
        """
        Update coral animation state.
        
        Args:
            delta_time (float): Time since last update
            health_value (float): Current health value (0-100)
        """
        self.time += delta_time * self.sway_speed
        self.color = self._get_health_color(health_value)

    def draw(self, screen):
        sway = math.sin(self.time + self.sway_offset) * 5
        
        if self.current_image:
            # Apply color tint to the image based on health
            tinted_image = self.current_image.copy()
            tinted_image.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT)
            
            # Calculate position with sway
            pos_x = self.x - tinted_image.get_width() // 2 + sway
            pos_y = self.y - tinted_image.get_height()
            
            # Draw the tinted image
            screen.blit(tinted_image, (pos_x, pos_y))
            
            # Add some particle effects for more life
            self._draw_particles(screen, sway)
        else:
            # Fallback to the original drawing method if no images are loaded
            if self.coral_type == 'brain':
                self._draw_brain_coral(screen, sway)
            else:
                self._draw_branching_coral(screen, sway)
            
            # Draw polyps
            for polyp in self.polyps:
                x = self.x + polyp['offset'][0] + sway * 0.5
                y = self.y + polyp['offset'][1]
                pygame.draw.circle(screen, self.color, (int(x), int(y)), int(polyp['size']))

    def _draw_branching_coral(self, screen, sway):
        for branch in self.branches:
            start_pos = (self.x, self.y)
            angle = branch['angle']
            length = branch['length']
            
            # Calculate end position with sway
            end_x = self.x + math.cos(angle) * length + sway
            end_y = self.y - math.sin(angle) * length
            end_pos = (int(end_x), int(end_y))
            
            # Draw main branch
            pygame.draw.line(screen, self.color, start_pos, end_pos, int(branch['thickness']))
            
            # Draw sub-branches
            for sub in branch['sub_branches']:
                sub_angle = angle + sub['angle']
                sub_length = sub['length']
                sub_end_x = end_x + math.cos(sub_angle) * sub_length + sway * 0.5
                sub_end_y = end_y - math.sin(sub_angle) * sub_length
                pygame.draw.line(screen, self.color, end_pos, 
                               (int(sub_end_x), int(sub_end_y)), 
                               int(sub['thickness']))

    def _draw_brain_coral(self, screen, sway):
        center_x = self.x + sway
        center_y = self.y
        
        # Draw main dome
        pygame.draw.ellipse(screen, self.color, 
                          (center_x - self.size/2, center_y - self.size/2, 
                           self.size, self.size))
        
        # Draw folds
        for branch in self.branches:
            fold_height = branch['length']
            for i in range(0, self.size, 8):
                x = center_x - self.size/2 + i
                y = center_y + math.sin(i * 0.1 + self.time) * fold_height
                pygame.draw.line(screen, self.color, 
                               (x, y), 
                               (x, y + fold_height), 
                               int(branch['thickness']))

    def _draw_particles(self, screen, sway):
        # Add subtle particle effects around the coral
        for _ in range(3):
            particle_x = self.x + random.uniform(-self.size/2, self.size/2) + sway
            particle_y = self.y - random.uniform(0, self.size)
            particle_size = random.uniform(1, 3)
            particle_alpha = random.randint(50, 150)
            
            particle_surface = pygame.Surface((int(particle_size*2), int(particle_size*2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color[:3], particle_alpha), 
                             (particle_size, particle_size), particle_size)
            screen.blit(particle_surface, (particle_x, particle_y))

class FishAnimation:
    def __init__(self, screen):
        self.screen = screen
        self.reset_position()
        self.speed = random.uniform(50, 100)
        # Initialize direction based on starting position
        self.direction = -1 if self.x > config.SCREEN_WIDTH/2 else 1  # Flip initial direction
        self.fish_count = random.randint(5, 8)
        self.vertical_speed = 0
        self.target_y = self.y
        self.schooling_timer = 0
        self.schooling_interval = random.uniform(3, 6)
        
        # Load fish images
        self.fish_images = self.load_fish_images()
        
        # Create fish instances with random images and positions
        self.fishes = []
        for _ in range(self.fish_count):
            self.fishes.append({
                'offset': (random.uniform(-30, 30), random.uniform(-20, 20)),
                'image': random.choice(self.fish_images),
                'scale': random.uniform(0.8, 1.2),
                'vertical_offset': random.uniform(-10, 10)
            })

    def reset_position(self):
        # Start position logic
        if random.random() < 0.5:
            self.x = -50  # Start from left
            self.direction = 1  # Move right
        else:
            self.x = config.SCREEN_WIDTH + 50  # Start from right
            self.direction = -1  # Move left
        self.y = random.randint(100, config.SCREEN_HEIGHT - 200)

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
        """
        Update fish animation based on time and coral health.
        
        Args:
            delta_time (float): Time since last update
            health_state (float): Current coral health (0-100)
        """
        # Update schooling behavior timer
        self.schooling_timer += delta_time
        if self.schooling_timer >= self.schooling_interval:
            self.schooling_timer = 0
            # Vary movement based on health
            if health_state > 70:
                # Happy, relaxed movement
                self.target_y = self.y + random.uniform(-50, 50)
                self.speed = random.uniform(50, 100)
            elif health_state > 30:
                # More erratic movement
                self.target_y = self.y + random.uniform(-100, 100)
                self.speed = random.uniform(100, 150)
            else:
                # Panicked movement
                self.target_y = self.y + random.uniform(-150, 150)
                self.speed = random.uniform(150, 200)
            
            # Keep fish within screen bounds
            self.target_y = max(50, min(config.SCREEN_HEIGHT - 150, self.target_y))
            self.schooling_interval = random.uniform(3, 6)

        # Smooth vertical movement
        y_diff = self.target_y - self.y
        self.vertical_speed = y_diff * 2 * delta_time
        self.y += self.vertical_speed

        # Horizontal movement
        speed_multiplier = 1.0
        if health_state < 30:
            speed_multiplier = 1.6  # Faster when coral is unhealthy
        elif health_state < 70:
            speed_multiplier = 1.3  # Slightly faster when coral is stressed

        self.x += self.speed * delta_time * self.direction * speed_multiplier

        # Reset position when off screen
        if (self.direction > 0 and self.x > config.SCREEN_WIDTH + 100) or \
           (self.direction < 0 and self.x < -100):
            self.reset_position()

    def draw(self, screen):
        for fish in self.fishes:
            # Calculate fish position with smooth movement
            fish_x = self.x + fish['offset'][0]
            fish_y = self.y + fish['offset'][1] + \
                    math.sin(self.x * 0.02 + fish['offset'][0] * 0.1) * 5 + \
                    fish['vertical_offset']
            
            # Get the fish image and scale it
            image = fish['image']
            scaled_size = (
                int(image.get_width() * fish['scale']),
                int(image.get_height() * fish['scale'])
            )
            scaled_image = pygame.transform.scale(image, scaled_size)
            
            # Flip image based on direction
            if self.direction > 0:  # Moving right
                scaled_image = pygame.transform.flip(scaled_image, True, False)
                
            # Draw the fish with alpha blending for smoother appearance
            scaled_image.set_alpha(240)
            screen.blit(scaled_image, 
                       (fish_x - scaled_size[0]/2, 
                        fish_y - scaled_size[1]/2)) 