import pygame
import config
import sys
from core.game_manager import GameManager

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 64)
        self.buttons = {
            "start": pygame.Rect(412, 300, 200, 50),
            "instructions": pygame.Rect(412, 400, 200, 50),
            "quit": pygame.Rect(412, 500, 200, 50)
        }
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    return self.handle_button_click(button_name)
        return None
                    
    def handle_button_click(self, button_name):
        if button_name == "start":
            return "start"
        elif button_name == "instructions":
            return "instructions"
        elif button_name == "quit":
            pygame.quit()
            sys.exit()
            
    def draw(self):
        # Draw title
        title = self.font.render("Coral Reef Survival Simulator", True, config.WHITE)
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH/2, 150))
        self.screen.blit(title, title_rect)
        
        # Draw buttons
        for button_name, button_rect in self.buttons.items():
            pygame.draw.rect(self.screen, config.WHITE, button_rect)
            button_text = self.font.render(button_name.title(), True, config.BLACK)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect) 