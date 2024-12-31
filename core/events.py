import random
import config

class Event:
    def __init__(self, name, description, duration, effects):
        self.name = name
        self.description = description
        self.duration = duration  # in seconds
        self.effects = effects
        self.time_remaining = duration

class EventSystem:
    def __init__(self):
        self.active_events = []
        self.time_until_next_event = random.uniform(10, 30)
        self.events_pool = self._create_events_pool()
        self.events_handled = 0  # Add this line to track handled events
        self.event_blocked = False  # For power-up functionality
        
    def _create_events_pool(self):
        return [
            Event("Heat Wave", 
                  "Water temperature is rising rapidly!", 
                  15, 
                  {"temperature": 2}),
            Event("Ocean Acidification", 
                  "pH levels are dropping!", 
                  12, 
                  {"ph": -0.3}),
            Event("Freshwater Influx", 
                  "Heavy rains are affecting salinity!", 
                  10, 
                  {"salinity": -2}),
            Event("Recovery Period", 
                  "Conditions are temporarily stabilizing.", 
                  8, 
                  {"health_boost": 5})
        ]
        
    def update(self, delta_time):
        # Update active events
        for event in self.active_events[:]:  # Create copy for safe removal
            event.time_remaining -= delta_time
            if event.time_remaining <= 0:
                self.active_events.remove(event)
                self.events_handled += 1  # Increment counter when event is handled
                
        # Check for new event
        self.time_until_next_event -= delta_time
        if self.time_until_next_event <= 0:
            self.trigger_random_event()
            self.time_until_next_event = random.uniform(10, 30)
            
    def trigger_random_event(self):
        if self.events_pool and len(self.active_events) < 2:  # Max 2 concurrent events
            event = random.choice(self.events_pool)
            self.active_events.append(event)
            return event
        return None
    
    def get_current_effects(self):
        """Returns combined effects of all active events"""
        combined_effects = {}
        for event in self.active_events:
            for effect_type, value in event.effects.items():
                combined_effects[effect_type] = combined_effects.get(effect_type, 0) + value
        return combined_effects 