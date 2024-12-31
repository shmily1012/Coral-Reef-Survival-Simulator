import pygame
import config

class TutorialOverlay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.active = True
        self.current_step = 0
        
        self.tutorial_steps = [
            "Welcome to Coral Reef Simulator!",
            "Control temperature, pH, and salinity to keep the coral healthy.",
            "Use the sliders below to adjust environmental conditions.",
            "Keep an eye on the health bar at the top.",
            "Watch out for environmental events!",
            "Complete 10 rounds to win.",
            "Click anywhere to start playing!"
        ]
        
    def next_step(self):
        self.current_step += 1
        if self.current_step >= len(self.tutorial_steps):
            self.active = False
            self.current_step = 0
            
    def draw(self):
        if not self.active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw current tutorial message
        if self.current_step < len(self.tutorial_steps):
            message = self.tutorial_steps[self.current_step]
            text = self.font.render(message, True, config.WHITE)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2))
            self.screen.blit(text, text_rect)
            
            # Draw "Click to continue" message
            continue_text = self.font.render("Click to continue", True, config.WHITE)
            continue_rect = continue_text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 + 50))
            self.screen.blit(continue_text, continue_rect) 