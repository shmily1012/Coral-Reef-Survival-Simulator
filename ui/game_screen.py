import pygame
import config
from visuals.background_manager import BackgroundManager
from core.facts_manager import FactsManager
from audio.sound_manager import SoundManager
from visuals.particle_system import ParticleSystem
from ui.tutorial_overlay import TutorialOverlay
from core.achievements import AchievementManager
from core.power_ups import PowerUpManager

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.active = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False
        elif event.type == pygame.MOUSEMOTION and self.active:
            self.value = self._get_value_from_mouse(event.pos[0])
            
    def _get_value_from_mouse(self, x):
        relative_x = (x - self.rect.x) / self.rect.width
        return self.min_val + (self.max_val - self.min_val) * relative_x
        
    def draw(self, screen):
        # Draw slider background
        pygame.draw.rect(screen, config.WHITE, self.rect)
        
        # Draw slider handle
        handle_pos = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_pos - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, config.BLACK, handle_rect)

class GameScreen:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.font = pygame.font.Font(None, 36)
        
        # Create sliders
        self.sliders = {
            "temperature": Slider(100, 500, 200, 20, config.TEMP_MIN, config.TEMP_MAX, config.TEMP_OPTIMAL),
            "ph": Slider(400, 500, 200, 20, config.PH_MIN, config.PH_MAX, config.PH_OPTIMAL),
            "salinity": Slider(700, 500, 200, 20, config.SALINITY_MIN, config.SALINITY_MAX, config.SALINITY_OPTIMAL)
        }
        
        self.background = BackgroundManager(screen)
        
        self.facts_manager = FactsManager()
        self.sound_manager = SoundManager()
        self.sound_manager.play_background_music()
        
        self.particle_system = ParticleSystem(screen)
        self.tutorial = TutorialOverlay(screen)
        
        self.achievement_manager = AchievementManager(screen)
        self.power_up_manager = PowerUpManager(screen, game_manager)
        
    def handle_event(self, event):
        if self.tutorial.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.tutorial.next_step()
            return
            
        for slider in self.sliders.values():
            slider.handle_event(event)
            
    def update(self, delta_time):
        """
        Update game state based on time passed since last frame.
        
        Args:
            delta_time: Time elapsed since last frame in seconds. Defaults to 1 second.
                       Used to ensure smooth animations and updates regardless of frame rate.
        """
        # Update game manager with slider values
        for action_type, slider in self.sliders.items():
            self.game_manager.handle_player_action(action_type, slider.value)
            
        self.background.update(delta_time, self.game_manager.health_system.current_health)
        
        self.facts_manager.update(delta_time)
        
        # Play sounds based on health changes
        current_health = self.game_manager.health_system.current_health
        if current_health < 30:
            self.sound_manager.play_sound("alert")
        
        self.particle_system.update(delta_time)
        
        # Create particles for events
        for event in self.game_manager.event_system.active_events:
            if "temperature" in event.effects:
                self.particle_system.create_warning_effect(150, 500)
            elif "ph" in event.effects:
                self.particle_system.create_warning_effect(450, 500)
            elif "salinity" in event.effects:
                self.particle_system.create_warning_effect(750, 500)
                
        self.power_up_manager.update(delta_time)
        
        # Update achievement state
        game_state = {
            "optimal_time": self.calculate_optimal_time(),
            "events_handled": self.game_manager.event_system.events_handled,
            "recovery_achieved": self.check_recovery()
        }
        self.achievement_manager.update(delta_time, game_state)
        self.achievement_manager.check_achievements(game_state)
    def calculate_optimal_time(self):
        # Check if all values are within optimal ranges
        temp_optimal = abs(self.sliders["temperature"].value - config.TEMP_OPTIMAL) < 1
        ph_optimal = abs(self.sliders["ph"].value - config.PH_OPTIMAL) < 0.2
        salinity_optimal = abs(self.sliders["salinity"].value - config.SALINITY_OPTIMAL) < 1
        
        if all([temp_optimal, ph_optimal, salinity_optimal]):
            return self.game_manager.time_elapsed
        return 0
        
    def check_recovery(self):
        health = self.game_manager.health_system.current_health
        return health > 70 and getattr(self, "_was_critical", False)
        
    def draw(self):
        # Draw health bar
        health = self.game_manager.health_system.current_health
        health_rect = pygame.Rect(50, 50, health * 3, 30)
        pygame.draw.rect(self.screen, config.GREEN, health_rect)
        
        # Draw sliders
        for name, slider in self.sliders.items():
            slider.draw(self.screen)
            label = self.font.render(f"{name}: {slider.value:.1f}", True, config.WHITE)
            self.screen.blit(label, (slider.rect.x, slider.rect.y - 30))
            
        # Draw active events
        y = 100
        for event in self.game_manager.event_system.active_events:
            text = self.font.render(event.description, True, config.WHITE)
            self.screen.blit(text, (50, y))
            y += 40 
        
        self.background.draw() 
        
        # Draw current fact if available
        fact = self.facts_manager.get_current_fact()
        if fact:
            fact_text = self.font.render(fact, True, config.WHITE)
            fact_rect = fact_text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT - 50))
            self.screen.blit(fact_text, fact_rect) 
        
        self.particle_system.draw()
        self.tutorial.draw() 
        
        self.achievement_manager.draw()
        self.power_up_manager.draw() 