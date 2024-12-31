import pygame
import sys
from core.game_manager import GameManager
from ui.main_menu import MainMenu
from visuals.visual_feedback import VisualFeedback
from ui.game_over_screen import GameOverScreen
from ui.game_screen import GameScreen
import config
from visuals.ocean_background import OceanBackground

class CoralReefSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Coral Reef Survival Simulator")
        
        # Initialize game components
        self.clock = pygame.time.Clock()
        self.game_manager = GameManager()
        self.screens = {
            "menu": MainMenu(self.screen),
            "game": GameScreen(self.screen, self.game_manager),
            "game_over": GameOverScreen(self.screen, self.game_manager)
        }
        self.visual_feedback = VisualFeedback(self.screen)
        self.ocean_background = OceanBackground(self.screen)
        self.current_screen = "menu"
        self.running = True

    def run(self):
        while self.running:
            delta_time = self.clock.tick(config.FPS) / 1000.0
            
            self.handle_events()
            self.update(delta_time)
            self.draw()
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            if self.current_screen == "menu":
                action = self.screens["menu"].handle_event(event)
                if action == "start":
                    self.current_screen = "game"
                    self.game_manager.start_game()
            
            elif self.current_screen == "game":
                self.screens["game"].handle_event(event)
            
            elif self.current_screen == "game_over":
                action = self.screens["game_over"].handle_event(event)
                if action == "restart":
                    self.current_screen = "game"
                    self.game_manager.start_game()
                elif action == "quit":
                    self.running = False
                
    def update(self, delta_time):
        self.ocean_background.update(delta_time)
        
        if self.current_screen == "game":
            self.game_manager.update(delta_time)
            self.screens["game"].update(delta_time)
            self.visual_feedback.update(delta_time)
            
            if self.game_manager.game_state == "game_over":
                self.current_screen = "game_over"
                
    def draw(self):
        self.ocean_background.draw()
        self.screens[self.current_screen].draw()
        
        if self.current_screen == "game":
            self.visual_feedback.draw()

if __name__ == "__main__":
    game = CoralReefSimulator()
    game.run() 