import pygame
import sys
from core.game_manager import GameManager
from ui.main_menu import MainMenu
from visuals.visual_feedback import VisualFeedback
from ui.game_over_screen import GameOverScreen
from ui.game_screen import GameScreen
import config

class CoralReefSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Coral Reef Survival Simulator")
        
        self.clock = pygame.time.Clock()
        self.game_manager = GameManager()
        self.main_menu = MainMenu(self.screen)
        self.running = True
        self.game_screen = GameScreen(self.screen, self.game_manager)
        self.game_over_screen = GameOverScreen(self.screen, self.game_manager)
        self.visual_feedback = VisualFeedback(self.screen)
        self.current_screen = "menu"  # menu, game, game_over

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_event(event)

            self.update(delta_time)
            self.draw()
            
            # Updates the full display surface to the screen
            # This line refreshes what's shown on screen with all the new drawings
            pygame.display.flip()   

        pygame.quit()
        sys.exit()
        
    def handle_event(self, event):
        if self.current_screen == "menu":
            action = self.main_menu.handle_event(event)
            if action == "start":
                self.current_screen = "game"
                self.game_manager.start_game()
        elif self.current_screen == "game":
            self.game_screen.handle_event(event)
        elif self.current_screen == "game_over":
            action = self.game_over_screen.handle_event(event)
            if action == "restart":
                self.current_screen = "game"
                self.game_manager.start_game()
            elif action == "quit":
                self.running = False
                
    def update(self, delta_time):
        if self.current_screen == "game":
            self.game_manager.update(delta_time)
            self.game_screen.update(delta_time)
            self.visual_feedback.update(delta_time)
            
            # Check for game over
            if self.game_manager.game_state == "game_over":
                self.current_screen = "game_over"
                
    def draw(self):
        self.screen.fill(config.OCEAN_BLUE)
        
        if self.current_screen == "menu":
            self.main_menu.draw()
        elif self.current_screen == "game":
            self.game_screen.draw()
            self.visual_feedback.draw()
        elif self.current_screen == "game_over":
            self.game_over_screen.draw()

if __name__ == "__main__":
    game = CoralReefSimulator()
    game.run() 