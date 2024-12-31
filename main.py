import pygame
import sys
from core.game_manager import GameManager
from ui.main_menu import MainMenu
from visuals.visual_feedback import VisualFeedback
from ui.game_over_screen import GameOverScreen
from ui.game_screen import GameScreen
import config
from visuals.ocean_background import OceanBackground
from ui.round_transition import RoundTransitionScreen
from utils.logger import logger

class CoralReefSimulator:
    def __init__(self):
        logger.info("Initializing Coral Reef Simulator")
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            pygame.display.set_caption("Coral Reef Survival Simulator")
            
            # Initialize game components
            self.clock = pygame.time.Clock()
            self.game_manager = GameManager()
            
            # Create screen dictionary with "playing" instead of "game"
            self.screens = {
                "menu": MainMenu(self.screen),
                "playing": GameScreen(self.screen, self.game_manager),  # Changed from "game" to "playing"
                "game_over": GameOverScreen(self.screen, self.game_manager),
                "round_end": RoundTransitionScreen(self.screen, self.game_manager)
            }
            self.visual_feedback = VisualFeedback(self.screen)
            self.ocean_background = OceanBackground(self.screen)
            self.running = True
            
            logger.debug("All game screens initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize game: {str(e)}")
            raise

    def run(self):
        logger.info("Starting game loop")
        while self.running:
            
            delta_time = self.clock.tick(config.FPS) / 1000.0
            self.handle_events()
            self.update(delta_time)
            self.draw()
            pygame.display.flip()
                
        # Clean up when game ends
        logger.info("Game shutting down")
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            # Use game_state directly from game_manager
            current_state = self.game_manager.game_state
            
            if current_state == "menu":
                action = self.screens["menu"].handle_event(event)
                if action == "start":
                    self.game_manager.start_game()
            
            elif current_state == "playing":  # Changed from "game" to "playing"
                self.screens["playing"].handle_event(event)  # Changed from "game" to "playing"
            
            elif current_state == "round_end":
                action = self.screens["round_end"].handle_event(event)
                if action == "menu":
                    self.game_manager.game_state = "menu"
            
            elif current_state == "game_over":
                action = self.screens["game_over"].handle_event(event)
                if action == "restart":
                    self.game_manager.start_game()
                elif action == "quit":
                    self.running = False
                
    def update(self, delta_time):
        self.ocean_background.update(delta_time)
        
        current_state = self.game_manager.game_state
        if current_state == "menu":
            self.screens["menu"].update()
        elif current_state == "playing":  # Changed from "game" to "playing"
            self.game_manager.update(delta_time)
            self.screens["playing"].update(delta_time)  # Changed from "game" to "playing"
            self.visual_feedback.update(delta_time)
        elif current_state == "round_end":
            self.screens["round_end"].update()
        elif current_state == "game_over":
            self.screens["game_over"].update()
                
    def draw(self):
        # Always draw the ocean background first
        self.ocean_background.draw()
        
        # Draw the current screen based on game state
        current_state = self.game_manager.game_state
        if current_state in self.screens:
            self.screens[current_state].draw()
        
        # Draw visual feedback only during gameplay
        if current_state == "playing":  # Changed from "game" to "playing"
            self.visual_feedback.draw()
            
        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    game = CoralReefSimulator()
    game.run() 