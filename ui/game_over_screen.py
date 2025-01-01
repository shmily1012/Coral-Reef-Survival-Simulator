import pygame
import config
from utils.logger import logger

class GameOverScreen:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 32)
        logger.info("GameOverScreen initialized")

    def handle_event(self, event):
        """Handle mouse clicks on game over screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if quit button was clicked
            quit_rect = pygame.Rect(config.SCREEN_WIDTH/2 - 100, config.SCREEN_HEIGHT/2 + 100, 200, 50)
            if quit_rect.collidepoint(mouse_pos):
                logger.info("Quit button clicked on game over screen")
                return "quit"
                
            # Check if restart button was clicked
            restart_rect = pygame.Rect(config.SCREEN_WIDTH/2 - 100, config.SCREEN_HEIGHT/2 + 20, 200, 50)
            if restart_rect.collidepoint(mouse_pos):
                logger.info("Restart button clicked on game over screen")
                return "restart"
        return None

    def update(self):
        """Update method to satisfy the interface requirement."""
        pass  # No updates needed for static game over screen

    def draw(self):
        """Draw the game over screen."""
        # Fill background
        self.screen.fill((0, 0, 0))  # Black background
        
        # Draw "Game Over" text
        game_over_text = self.font.render("Game Over", True, config.WHITE)
        text_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/3))
        self.screen.blit(game_over_text, text_rect)
        
        # Draw final score
        score_text = self.small_font.render(f"Final Score: {self.game_manager.score}", True, config.WHITE)
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 - 50))
        self.screen.blit(score_text, score_rect)
        
        # Draw restart button
        restart_rect = pygame.Rect(config.SCREEN_WIDTH/2 - 100, config.SCREEN_HEIGHT/2 + 20, 200, 50)
        pygame.draw.rect(self.screen, config.GREEN, restart_rect)
        restart_text = self.small_font.render("Restart", True, config.BLACK)
        restart_text_rect = restart_text.get_rect(center=restart_rect.center)
        self.screen.blit(restart_text, restart_text_rect)
        
        # Draw quit button
        quit_rect = pygame.Rect(config.SCREEN_WIDTH/2 - 100, config.SCREEN_HEIGHT/2 + 100, 200, 50)
        pygame.draw.rect(self.screen, config.RED, quit_rect)
        quit_text = self.small_font.render("Quit", True, config.BLACK)
        quit_text_rect = quit_text.get_rect(center=quit_rect.center)
        self.screen.blit(quit_text, quit_text_rect) 