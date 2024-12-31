from core.health_system import HealthSystem
from core.events import EventSystem
from core.player_actions import PlayerActions
import config
from utils.logger import logger

"""
Game Manager Module

Central manager for game state, handling rounds, timing, and game progression.

Features:
- Round management (10 rounds)
- Timer system
- Difficulty progression
- Game state transitions
- Score tracking
"""

class GameManager:
    def __init__(self):
        logger.info("Initializing GameManager")
        self.difficulty = "normal"
        self.settings = config.DIFFICULTY_SETTINGS[self.difficulty]
        self.health_system = HealthSystem()
        self.event_system = EventSystem()
        self.player_actions = PlayerActions()
        self.game_state = "menu"  # States: menu, playing, round_end, game_over
        self.score = 0
        self.time_elapsed = 0
        
        # Round management
        self.current_round = 1
        self.TOTAL_ROUNDS = config.TOTAL_ROUNDS
        self.round_timer = config.ROUND_DURATION  # Use config value
        
        # Control management
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
        self.CONTROL_RELEASE_TIME = 0.5
        
    def start_game(self):
        """Initialize a new game."""
        logger.info(f"Starting new game with difficulty: {self.difficulty}")
        self.game_state = "playing"
        self.health_system.reset()
        self.score = 0
        self.time_elapsed = 0
        self.current_round = 1
        self.round_timer = config.ROUND_DURATION
        
        # Reset environmental factors to optimal
        self.health_system.temperature = config.TEMP_OPTIMAL
        self.health_system.ph = config.PH_OPTIMAL
        self.health_system.salinity = config.SALINITY_OPTIMAL
        
        # Reset event system
        self.event_system = EventSystem()
        
        # Log game start
        logger.info("Game started with initial settings:")
        logger.info(f"Health: {self.health_system.current_health}")
        logger.info(f"Round: {self.current_round}/{self.TOTAL_ROUNDS}")
        logger.info(f"Timer: {self.round_timer}")
        
    def start_next_round(self):
        """Start the next round."""
        self.current_round += 1
        self.round_timer = config.ROUND_DURATION  # Use config value
        self.game_state = "playing"
        
        # Keep the same health from last round
        self.health_system.current_health = self.last_round_health
        
        # Reset environmental factors to optimal
        self.health_system.temperature = config.TEMP_OPTIMAL
        self.health_system.ph = config.PH_OPTIMAL
        self.health_system.salinity = config.SALINITY_OPTIMAL
        
        # Adjust difficulty
        self.adjust_difficulty()
        
    def adjust_difficulty(self):
        """Increase difficulty as rounds progress."""
        # Example: Increase event frequency and damage
        event_multiplier = 1.0 + (self.current_round - 1) * 0.1  # 10% increase per round
        self.event_system.adjust_difficulty(event_multiplier)
        
    def update(self, delta_time):
        if self.game_state != "playing":
            return
            
        # Update round timer
        self.round_timer -= delta_time
        if self.round_timer <= 0:
            self.handle_round_end()
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
        
    def handle_round_end(self):
        """Handle the end of a round."""
        logger.info(f"Round {self.current_round} completed. Score: {self.score}")
        round_score = int(self.health_system.current_health)
        self.score += round_score
        
        if self.current_round >= self.TOTAL_ROUNDS:
            logger.info(f"Game completed! Final score: {self.score}")
            self.game_state = "game_over"
        else:
            self.last_round_health = self.health_system.current_health
            self.game_state = "round_end"
            
    def get_round_info(self):
        """Get current round information for display."""
        return {
            "current_round": self.current_round,
            "total_rounds": self.TOTAL_ROUNDS,
            "time_remaining": max(0, self.round_timer),
            "score": self.score
        } 