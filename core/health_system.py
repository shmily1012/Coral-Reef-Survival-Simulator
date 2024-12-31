import config

"""
Health System Module

Manages the coral reef's health status and environmental conditions.
Tracks and updates health based on various environmental factors and handles
health regeneration when conditions are optimal.

Features:
- Health tracking and state management
- Environmental factor monitoring (temperature, pH, salinity)
- Damage calculation from suboptimal conditions
- Health regeneration under optimal conditions
"""

class HealthSystem:
    def __init__(self):
        self.current_health = config.INITIAL_HEALTH
        self.max_health = 100
        self.temperature = config.TEMP_OPTIMAL
        self.ph = config.PH_OPTIMAL
        self.salinity = config.SALINITY_OPTIMAL
        
    def decrease_health(self, amount):
        self.current_health = max(0, self.current_health - amount)
        
    def increase_health(self, amount):
        # Only allow healing if not at max health
        if self.current_health < self.max_health:
            self.current_health = min(self.max_health, self.current_health + amount)
            
    def get_health_state(self):
        if self.current_health >= 70:
            return "healthy"
        elif self.current_health >= 30:
            return "stressed"
        else:
            return "bleached"
            
    def reset(self):
        self.current_health = config.INITIAL_HEALTH
        self.temperature = config.TEMP_OPTIMAL
        self.ph = config.PH_OPTIMAL
        self.salinity = config.SALINITY_OPTIMAL

    def update(self, delta_time):
        # Natural health decrease over time
        # self.current_health -= config.HEALTH_DECREASE_RATE * delta_time
        
        # Check environmental factors
        self.apply_temperature_effects(delta_time)
        self.apply_ph_effects(delta_time)
        self.apply_salinity_effects(delta_time)
        
        # Clamp health between 0 and max_health
        self.current_health = max(0, min(self.max_health, self.current_health))
        
    def apply_temperature_effects(self, delta_time):
        temp_diff = abs(self.temperature - config.TEMP_OPTIMAL)
        if temp_diff > 2:
            self.current_health -= temp_diff * 2 * delta_time
    def apply_ph_effects(self, delta_time):
        ph_diff = abs(self.ph - config.PH_OPTIMAL)
        if ph_diff > 0.3:
            self.current_health -= ph_diff * 4 * delta_time
            
    def apply_salinity_effects(self, delta_time):
        salinity_diff = abs(self.salinity - config.SALINITY_OPTIMAL)
        if salinity_diff > 1:
            self.current_health -= salinity_diff * 3 * delta_time
            
    def apply_player_action(self, action_type, value):
        if action_type == "temperature":
            self.temperature = value
        elif action_type == "ph":
            self.ph = value
        elif action_type == "salinity":
            self.salinity = value
    
