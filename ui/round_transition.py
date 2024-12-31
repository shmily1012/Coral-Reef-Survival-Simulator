"""
Round Transition Screen Module

Handles the interface between game rounds, showing round summary
and providing options to continue or pause the game.

Features:
- Round summary display
- Score display
- Continue/Pause options
- Visual feedback
"""

import pygame
import config

class RoundTransitionScreen:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.font_large = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        
        # Button dimensions and positions
        button_width = 200
        button_height = 50
        button_y = config.SCREEN_HEIGHT * 0.7
        
        # Create continue button
        self.continue_button = pygame.Rect(
            config.SCREEN_WIDTH/2 - button_width - 20,
            button_y,
            button_width,
            button_height
        )
        
        # Create pause button
        self.pause_button = pygame.Rect(
            config.SCREEN_WIDTH/2 + 20,
            button_y,
            button_width,
            button_height
        )
        
        self.button_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        
        # Initialize hover states
        self.continue_hover = False
        self.pause_hover = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.continue_button.collidepoint(mouse_pos):
                self.game_manager.start_next_round()
                return "playing"
                
            elif self.pause_button.collidepoint(mouse_pos):
                return "menu"
                
        return "round_end"
        
    def update(self):
        # Update hover states
        mouse_pos = pygame.mouse.get_pos()
        self.continue_hover = self.continue_button.collidepoint(mouse_pos)
        self.pause_hover = self.pause_button.collidepoint(mouse_pos)
        
    def draw(self):
        # Fill background
        self.screen.fill(config.OCEAN_BLUE)
        
        # Draw round completion text
        round_text = f"Round {self.game_manager.current_round} Complete!"
        text_surface = self.font_large.render(round_text, True, config.WHITE)
        text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT * 0.3))
        self.screen.blit(text_surface, text_rect)
        
        # Draw score
        score_text = f"Round Score: {self.game_manager.health_system.current_health}"
        score_surface = self.font.render(score_text, True, config.WHITE)
        score_rect = score_surface.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT * 0.4))
        self.screen.blit(score_surface, score_rect)
        
        total_score_text = f"Total Score: {self.game_manager.score}"
        total_score_surface = self.font.render(total_score_text, True, config.WHITE)
        total_score_rect = total_score_surface.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT * 0.5))
        self.screen.blit(total_score_surface, total_score_rect)
        
        # Draw continue button
        pygame.draw.rect(self.screen, 
                        self.hover_color if self.continue_hover else self.button_color, 
                        self.continue_button)
        continue_text = self.font.render("Continue", True, config.WHITE)
        continue_rect = continue_text.get_rect(center=self.continue_button.center)
        self.screen.blit(continue_text, continue_rect)
        
        # Draw pause button
        pygame.draw.rect(self.screen, 
                        self.hover_color if self.pause_hover else self.button_color, 
                        self.pause_button)
        pause_text = self.font.render("Pause", True, config.WHITE)
        pause_rect = pause_text.get_rect(center=self.pause_button.center)
        self.screen.blit(pause_text, pause_rect) 