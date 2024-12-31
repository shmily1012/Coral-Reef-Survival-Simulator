import pygame
import config
from visuals.background_manager import BackgroundManager
from visuals.animations import CoralAnimation, FishAnimation
from core.facts_manager import FactsManager
from audio.sound_manager import SoundManager
from visuals.particle_system import ParticleSystem
from ui.tutorial_overlay import TutorialOverlay
from core.achievements import AchievementManager
from core.power_ups import PowerUpManager
from utils.logger import logger
import math

"""
Game Screen Module

Main game interface that handles the visual representation and user interaction.
Manages sliders for environmental controls, displays health and event information,
and coordinates various visual elements.

Features:
- Environmental control sliders
- Health bar display
- Event notifications
- Particle effects
- Sound management
- Achievement tracking
"""

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
        logger.info("Initializing GameScreen")
        
        self.screen = screen
        self.game_manager = game_manager
        self.font = pygame.font.Font(None, 36)
        
        try:
            # Initialize background first
            logger.debug("Initializing BackgroundManager")
            self.background = BackgroundManager(screen)
            
            # Create coral animations
            logger.debug("Creating coral animations")
            self.corals = [
                CoralAnimation(x, config.SCREEN_HEIGHT - 100) 
                for x in range(100, config.SCREEN_WIDTH - 100, 150)
            ]
            logger.info(f"Created {len(self.corals)} coral animations")
            
            # Create fish schools
            logger.debug("Creating fish schools")
            self.fish_schools = [
                FishAnimation(screen) for _ in range(3)
            ]
            logger.info(f"Created {len(self.fish_schools)} fish schools")
            
            # Create sliders
            logger.debug("Initializing environmental control sliders")
            self.sliders = {
                "temperature": Slider(100, 500, 200, 20, config.TEMP_MIN, config.TEMP_MAX, config.TEMP_OPTIMAL),
                "ph": Slider(400, 500, 200, 20, config.PH_MIN, config.PH_MAX, config.PH_OPTIMAL),
                "salinity": Slider(700, 500, 200, 20, config.SALINITY_MIN, config.SALINITY_MAX, config.SALINITY_OPTIMAL)
            }
            
            # Initialize other managers
            logger.debug("Initializing game managers")
            self.facts_manager = FactsManager()
            self.sound_manager = SoundManager()
            self.particle_system = ParticleSystem(screen)
            self.achievement_manager = AchievementManager(screen)
            self.power_up_manager = PowerUpManager(screen, game_manager)
            
            # Initialize tutorial
            logger.debug("Initializing tutorial overlay")
            self.tutorial = TutorialOverlay(screen)
            self.tutorial.active = True
            
            # Start background music
            logger.debug("Starting background music")
            self.sound_manager.play_background_music()
            
            # Add timer for health regeneration
            self.optimal_condition_timer = 0
            self.REGEN_DELAY = 5.0
            self.REGEN_RATE = 1.0
            
            logger.info("GameScreen initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Error during GameScreen initialization: {str(e)}", exc_info=True)
            raise

    def handle_event(self, event):
        # Handle tutorial first
        if self.tutorial.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.tutorial.next_step()
            return
            
        # Handle other events only if tutorial is not active
        for slider in self.sliders.values():
            slider.handle_event(event)
            
    def update(self, delta_time):
        """Update game state based on time passed since last frame."""
        # Get current health for animations
        current_health = self.game_manager.health_system.current_health
        
        # Always allow player control through sliders
        for action_type, slider in self.sliders.items():
            if slider.active:  # When player is actively moving the slider
                self.game_manager.handle_player_action(action_type, slider.value)
            else:  # When slider is not being controlled, update it to show current value
                current_value = getattr(self.game_manager.health_system, action_type)
                slider.value = current_value
        
        # Check conditions and update health regeneration
        if self.check_optimal_conditions():
            self.optimal_condition_timer += delta_time
            if self.optimal_condition_timer >= self.REGEN_DELAY:
                # Increase health by 1 per second
                self.game_manager.health_system.increase_health(self.REGEN_RATE * delta_time)
        else:
            # Reset timer if conditions are not optimal
            self.optimal_condition_timer = 0
            
        # Update animations and visual elements
        for school in self.fish_schools:
            school.update(delta_time, current_health)  # Pass health state to fish animations
            
        for coral in self.corals:
            coral.update(delta_time, current_health)
            
        self.background.update(delta_time, current_health)
        
        self.facts_manager.update(delta_time)
        
        # Play sounds based on health changes
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
        
        # Handle warning sounds
        if self.game_manager.event_system.is_warning:
            self.sound_manager.play_warning()
        else:
            self.sound_manager.reset_warning()
        
    def check_optimal_conditions(self):
        """Check if environmental conditions are optimal for coral health regeneration."""
        temp_optimal = abs(self.sliders["temperature"].value - config.TEMP_OPTIMAL) < config.HEALTH_REGEN_THRESHOLDS["temperature"]
        ph_optimal = abs(self.sliders["ph"].value - config.PH_OPTIMAL) < config.HEALTH_REGEN_THRESHOLDS["ph"]
        salinity_optimal = abs(self.sliders["salinity"].value - config.SALINITY_OPTIMAL) < config.HEALTH_REGEN_THRESHOLDS["salinity"]
        
        return all([temp_optimal, ph_optimal, salinity_optimal])
        
    def calculate_health_regeneration(self, delta_time):
        """Calculate health regeneration rate based on current conditions."""
        base_regen_rate = 5.0  # Health points per second
        current_health = self.game_manager.health_system.current_health
        
        # Reduce regeneration rate as health gets higher
        health_factor = 1.0 - (current_health / 100.0)
        
        return base_regen_rate * health_factor * delta_time
        
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
        # Clear the screen first
        self.screen.fill(config.OCEAN_BLUE)
        
        # Draw background
        self.background.draw()
        
        # Draw corals
        for coral in self.corals:
            coral.draw(self.screen)
        
        # Draw fish schools
        for school in self.fish_schools:
            school.draw(self.screen)
        
        # Draw health bar
        health = self.game_manager.health_system.current_health
        health_bar_bg = pygame.Rect(50, 50, 300, 30)
        pygame.draw.rect(self.screen, (100, 0, 0), health_bar_bg)
        health_rect = pygame.Rect(50, 50, health * 3, 30)
        health_color = self.get_health_color(health)
        pygame.draw.rect(self.screen, health_color, health_rect)
        
        # Draw health text
        health_text = f"{int(health)}/100 ({int(health)}%)"
        health_value = self.font.render(health_text, True, config.WHITE)
        text_rect = health_value.get_rect(midleft=(health_bar_bg.right + 10, health_bar_bg.centery))
        self.screen.blit(health_value, text_rect)
        
        # Draw sliders
        for name, slider in self.sliders.items():
            slider.draw(self.screen)
            label = pygame.font.SysFont('arial', 24).render(f"{name}: {slider.value:.1f}", True, config.WHITE)
            self.screen.blit(label, (slider.rect.x, slider.rect.y - 30))
        
        # Draw events and warnings
        y = 100
        warning = self.game_manager.event_system.get_warning_message()
        if warning:
            warning_text = self.font.render(warning, True, (255, 255, 0))
            warning_rect = warning_text.get_rect(center=(config.SCREEN_WIDTH/2, y))
            self.screen.blit(warning_text, warning_rect)
            y += 40
        
        # Draw active events
        for event in self.game_manager.event_system.active_events:
            text = self.font.render(event.description, True, config.WHITE)
            self.screen.blit(text, (50, y))
            y += 40
        
        # Draw current fact
        fact = self.facts_manager.get_current_fact()
        if fact:
            fact_text = self.font.render(fact, True, config.WHITE)
            fact_rect = fact_text.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT - 50))
            self.screen.blit(fact_text, fact_rect)
        
        # Draw round information
        round_info = self.game_manager.get_round_info()
        round_text = f"Round {round_info['current_round']}/{round_info['total_rounds']}"
        time_text = f"Time: {int(round_info['time_remaining'])}s"
        score_text = f"Score: {round_info['score']}"
        
        self.screen.blit(self.font.render(round_text, True, config.WHITE), (10, 10))
        self.screen.blit(self.font.render(time_text, True, config.WHITE), (config.SCREEN_WIDTH - 150, 10))
        self.screen.blit(self.font.render(score_text, True, config.WHITE), (config.SCREEN_WIDTH//2 - 50, 10))
        
        # Draw particles
        self.particle_system.draw()
        
        # Draw tutorial overlay last
        if self.tutorial.active:
            self.tutorial.draw()
        
    def draw_regen_timer(self, progress):
        """Draw a circular progress indicator for regeneration timer."""
        center_x = config.SCREEN_WIDTH - 50
        center_y = 50
        radius = 20
        
        # Draw background circle
        pygame.draw.circle(self.screen, config.WHITE, (center_x, center_y), radius)
        
        # Draw progress arc
        angle = progress * 360
        rect = pygame.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)
        pygame.draw.arc(self.screen, config.GREEN, rect, 0, math.radians(angle), 3)
        
        # Draw timer text
        if progress < 1:
            time_left = math.ceil(self.REGEN_DELAY - self.optimal_condition_timer)
            text = self.font.render(str(time_left), True, config.BLACK)
            text_rect = text.get_rect(center=(center_x, center_y))
            self.screen.blit(text, text_rect) 
        
    def get_health_color(self, health):
        """Return color based on health value."""
        if health >= 70:
            return config.GREEN
        elif health >= 30:
            return (255, 165, 0)  # Orange
        else:
            return config.RED 