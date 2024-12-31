from core.health_system import HealthSystem
from core.events import EventSystem
from core.player_actions import PlayerActions
import config

class GameManager:
    def __init__(self):
        self.difficulty = "normal"
        self.settings = config.DIFFICULTY_SETTINGS[self.difficulty]
        self.health_system = HealthSystem()
        self.event_system = EventSystem()
        self.player_actions = PlayerActions()
        self.game_state = "menu"  # States: menu, playing, game_over
        self.score = 0
        self.time_elapsed = 0
        self.player_controlled = {
            "temperature": False,
            "ph": False,
            "salinity": False
        }
        self.control_timeout = {
            "temperature": 0,
            "ph": 0,
            "salinity": 0
        }
        self.CONTROL_RELEASE_TIME = 0.5  # Time in seconds before events can affect a value after player releases control
        
    def start_game(self):
        self.game_state = "playing"
        self.health_system.reset()
        self.score = 0
        self.time_elapsed = 0
        
    def update(self, delta_time):
        if self.game_state != "playing":
            return
            
        # Update event system
        self.event_system.update(delta_time)
        
        # Update control timeouts
        for factor in self.control_timeout:
            if self.control_timeout[factor] > 0:
                self.control_timeout[factor] -= delta_time
                if self.control_timeout[factor] <= 0:
                    self.player_controlled[factor] = False
        
        # Apply event effects only to factors not being controlled by player
        event_effects = self.event_system.get_current_effects()
        for factor, change in event_effects.items():
            if not self.player_controlled[factor] and self.control_timeout[factor] <= 0:
                current_value = getattr(self.health_system, factor)
                new_value = current_value + change * delta_time
                
                # Clamp values to their valid ranges
                if factor == "temperature":
                    new_value = max(config.TEMP_MIN, min(config.TEMP_MAX, new_value))
                elif factor == "ph":
                    new_value = max(config.PH_MIN, min(config.PH_MAX, new_value))
                elif factor == "salinity":
                    new_value = max(config.SALINITY_MIN, min(config.SALINITY_MAX, new_value))
                    
                setattr(self.health_system, factor, new_value)
        
        # Update health system
        self.health_system.update(delta_time)
        self.time_elapsed += delta_time
        
        # Check win/lose conditions
        if self.health_system.current_health <= 0:
            self.game_state = "game_over"
            
    def handle_player_action(self, action_type, value):
        if self.game_state != "playing":
            return
            
        # Mark the factor as player-controlled and set timeout
        self.player_controlled[action_type] = True
        self.control_timeout[action_type] = self.CONTROL_RELEASE_TIME
        
        # Apply the player's action
        self.player_actions.process_action(action_type, value)
        self.health_system.apply_player_action(action_type, value)
        
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.settings = config.DIFFICULTY_SETTINGS[difficulty] 