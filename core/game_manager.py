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
        
    def start_game(self):
        self.game_state = "playing"
        self.health_system.reset()
        self.score = 0
        self.time_elapsed = 0
        
    def update(self, delta_time):
        if self.game_state != "playing":
            return
            
        self.time_elapsed += delta_time
        
        # Update systems with difficulty settings
        self.event_system.update(delta_time * self.settings["event_frequency"])
        self.health_system.update(delta_time * self.settings["health_decrease_rate"])
        
        # Check win/lose conditions
        if self.health_system.current_health <= 0:
            self.game_state = "game_over"
            
    def handle_player_action(self, action_type, value):
        if self.game_state != "playing":
            return
            
        self.player_actions.process_action(action_type, value)
        self.health_system.apply_player_action(action_type, value) 
        
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.settings = config.DIFFICULTY_SETTINGS[difficulty] 