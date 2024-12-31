import config

class PlayerActions:
    def __init__(self):
        self.temperature = config.TEMP_OPTIMAL
        self.ph = config.PH_OPTIMAL
        self.salinity = config.SALINITY_OPTIMAL
        
    def process_action(self, action_type, value):
        """Process and validate player actions"""
        if action_type == "temperature":
            self.temperature = self._clamp(value, config.TEMP_MIN, config.TEMP_MAX)
        elif action_type == "ph":
            self.ph = self._clamp(value, config.PH_MIN, config.PH_MAX)
        elif action_type == "salinity":
            self.salinity = self._clamp(value, config.SALINITY_MIN, config.SALINITY_MAX)
            
    def _clamp(self, value, min_val, max_val):
        """Ensure value stays within allowed range"""
        return max(min_val, min(value, max_val))
    
    def get_current_values(self):
        """Return current environmental values"""
        return {
            "temperature": self.temperature,
            "ph": self.ph,
            "salinity": self.salinity
        } 