import pygame
import config

class TutorialOverlay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.current_step = 0
        self.steps = [
            {
                "text": "Welcome to the Coral Reef Simulator! Let's learn how to protect our reef.",
                "highlight": None
            },
            {
                "text": "This is the temperature control. Keep it between 23-29°C.",
                "highlight": "temperature"
            },
            {
                "text": "Monitor the pH level here. Aim for 8.0-8.4.",
                "highlight": "ph"
            },
            {
                "text": "Watch the salinity. Keep it between 32-36 ppt.",
                "highlight": "salinity"
            },
            {
                "text": "Random events will occur! React quickly to protect the reef.",
                "highlight": None
            }
        ]
        self.active = False
        
    def start(self):
        self.active = True
        self.current_step = 0
        
    def next_step(self):
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.active = False
            
    def draw(self):
        if not self.active or self.current_step >= len(self.steps):
            return
            
        step = self.steps[self.current_step]
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw text box
        text = self.font.render(step["text"], True, config.WHITE)
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT - 100))
        pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 20))
        self.screen.blit(text, text_rect)
        
        # Draw continue prompt
        continue_text = self.font.render("Click to continue...", True, config.WHITE)
        continue_rect = continue_text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT - 50))
        self.screen.blit(continue_text, continue_rect) 