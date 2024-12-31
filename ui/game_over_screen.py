import pygame
import config

class GameOverScreen:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Create buttons
        self.buttons = {
            "restart": pygame.Rect(362, 400, 300, 50),
            "quit": pygame.Rect(362, 500, 300, 50)
        }
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(mouse_pos):
                    return self.handle_button_click(button_name)
        return None
                    
    def handle_button_click(self, button_name):
        if button_name == "restart":
            return "restart"
        elif button_name == "quit":
            return "quit"
            
    def draw(self):
        # Draw game over message
        title = self.font_large.render("Game Over!", True, config.WHITE)
        title_rect = title.get_rect(center=(config.SCREEN_WIDTH/2, 150))
        self.screen.blit(title, title_rect)
        
        # Draw final score
        score_text = self.font_medium.render(
            f"Time Survived: {self.game_manager.time_elapsed:.1f} seconds", 
            True, 
            config.WHITE
        )
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH/2, 250))
        self.screen.blit(score_text, score_rect)
        
        # Draw educational message
        message = self.get_educational_message()
        message_text = self.font_small.render(message, True, config.WHITE)
        message_rect = message_text.get_rect(center=(config.SCREEN_WIDTH/2, 320))
        self.screen.blit(message_text, message_rect)
        
        # Draw buttons
        for button_name, button_rect in self.buttons.items():
            pygame.draw.rect(self.screen, config.WHITE, button_rect)
            button_text = self.font_medium.render(button_name.title(), True, config.BLACK)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
            
    def get_educational_message(self):
        """Returns an educational message based on game performance"""
        if self.game_manager.time_elapsed < 30:
            return "Tip: Try to keep environmental values close to optimal levels!"
        elif self.game_manager.time_elapsed < 60:
            return "Remember: Coral reefs are sensitive to temperature changes!"
        else:
            return "Great job! You're helping protect our coral reefs!" 