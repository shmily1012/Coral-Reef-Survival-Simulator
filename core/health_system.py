import config

class HealthSystem:
    def __init__(self):
        self.current_health = config.INITIAL_HEALTH
        self.temperature = config.TEMP_OPTIMAL
        self.ph = config.PH_OPTIMAL
        self.salinity = config.SALINITY_OPTIMAL
        
    def reset(self):
        self.current_health = config.INITIAL_HEALTH
        self.temperature = config.TEMP_OPTIMAL
        self.ph = config.PH_OPTIMAL
        self.salinity = config.SALINITY_OPTIMAL
        
    def update(self, delta_time):
        # Natural health decrease over time
        self.current_health -= config.HEALTH_DECREASE_RATE * delta_time
        
        # Check environmental factors
        self.apply_temperature_effects()
        self.apply_ph_effects()
        self.apply_salinity_effects()
        
        # Clamp health between 0 and 100
        self.current_health = max(0, min(100, self.current_health))
        
    def apply_temperature_effects(self):
        temp_diff = abs(self.temperature - config.TEMP_OPTIMAL)
        if temp_diff > 2:
            self.current_health -= temp_diff * 0.1
            
    def apply_ph_effects(self):
        ph_diff = abs(self.ph - config.PH_OPTIMAL)
        if ph_diff > 0.3:
            self.current_health -= ph_diff * 0.2
            
    def apply_salinity_effects(self):
        salinity_diff = abs(self.salinity - config.SALINITY_OPTIMAL)
        if salinity_diff > 1:
            self.current_health -= salinity_diff * 0.15
            
    def apply_player_action(self, action_type, value):
        if action_type == "temperature":
            self.temperature = value
        elif action_type == "ph":
            self.ph = value
        elif action_type == "salinity":
            self.salinity = value 