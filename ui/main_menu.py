import pygame
import config
import sys
from core.game_manager import GameManager

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        
        # Create start button
        button_width = 200
        button_height = 50
        self.start_button = pygame.Rect(
            config.SCREEN_WIDTH/2 - button_width/2,
            config.SCREEN_HEIGHT/2 - button_height/2,
            button_width,
            button_height
        )
        
        self.button_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.hover = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return "start"
        return None
        
    def update(self):
        self.hover = self.start_button.collidepoint(pygame.mouse.get_pos())
        
    def draw(self):
        self.screen.fill(config.OCEAN_BLUE)
        
        # Draw title
        title = self.font.render("Coral Reef Simulator", True, config.WHITE)
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/3))
        self.screen.blit(title, title_rect)
        
        # Draw start button
        pygame.draw.rect(self.screen, 
                        self.hover_color if self.hover else self.button_color,
                        self.start_button)
        start_text = self.font.render("Start", True, config.WHITE)
        text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, text_rect) 