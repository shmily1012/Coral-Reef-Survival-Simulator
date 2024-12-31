import pygame
import config

class VisualEffect:
    def __init__(self, x, y, text, color, duration=2.0):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.duration = duration
        self.time_remaining = duration
        self.font = pygame.font.Font(None, 24)
        
    def update(self, delta_time):
        self.time_remaining -= delta_time
        return self.time_remaining <= 0
        
    def draw(self, screen):
        alpha = int(255 * (self.time_remaining / self.duration))
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (self.x, self.y))

class VisualFeedback:
    def __init__(self, screen):
        self.screen = screen
        self.effects = []
        
    def add_effect(self, x, y, text, color=config.WHITE):
        self.effects.append(VisualEffect(x, y, text, color))
        
    def add_health_change(self, x, y, amount):
        text = f"{amount:+.1f}"
        color = config.GREEN if amount > 0 else config.RED
        self.add_effect(x, y, text, color)
        
    def update(self, delta_time):
        # Update and remove finished effects
        self.effects = [effect for effect in self.effects 
                       if not effect.update(delta_time)]
        
    def draw(self):
        for effect in self.effects:
            effect.draw(self.screen) 