"""
Event System Module

This module manages environmental events that affect the coral reef ecosystem.
It handles the creation, timing, and effects of various events like temperature changes,
pH fluctuations, and salinity variations.

Key Features:
- Event scheduling with warning system
- Single event at a time to prevent overwhelming players
- Cooldown periods between events
- Warning notifications before events occur
"""

import random
import config
from utils.logger import logger, log_exception

class Event:
    """
    Represents a single environmental event affecting the coral reef.
    
    Attributes:
        description (str): Human-readable description of the event
        effects (dict): Environmental effects of the event (temperature, pH, salinity)
        duration (float): How long the event lasts in seconds
        time_remaining (float): Time until event ends
        cooldown (float): Minimum time before next event can start
    """
    def __init__(self, description, effects):
        self.description = description
        self.effects = effects
        self.duration = random.uniform(5.0, 8.0)  # Events last 5-8 seconds
        self.time_remaining = self.duration
        self.cooldown = 10.0  # Increased cooldown to 10 seconds minimum

class EventSystem:
    def __init__(self):
        self.active_events = []
        self.event_timer = 0
        self.event_interval = random.uniform(15.0, 20.0)  # Longer interval between events
        self.events_handled = 0
        self.cooldown_timer = 0
        self.min_gap_between_events = 10.0  # Minimum time between events
        self.warning_time = 5.0  # 5 second warning before event
        self.pending_event = None  # Store the upcoming event
        self.is_warning = False  # Track if we're in warning phase
        self.difficulty_multiplier = 1.0  # Add difficulty multiplier
        
        # Define possible events and their effects
        self.possible_events = [
            {
                "description": "Heat wave approaching!",
                "effects": {"temperature": 3.0}
            },
            {
                "description": "Cold current detected!",
                "effects": {"temperature": -3.0}
            },
            {
                "description": "Acid rain affecting the area!",
                "effects": {"ph": -0.5}
            },
            {
                "description": "Agricultural runoff detected!",
                "effects": {"ph": 0.3}
            },
            {
                "description": "Heavy rainfall reducing salinity!",
                "effects": {"salinity": -2.0}
            },
            {
                "description": "Increased evaporation!",
                "effects": {"salinity": 2.0}
            }
        ]

    def adjust_difficulty(self, multiplier):
        """
        Adjust the difficulty of events.
        
        Args:
            multiplier (float): Multiplier for event effects and frequency
        """
        logger.info(f"Adjusting event difficulty with multiplier: {multiplier}")
        self.difficulty_multiplier = multiplier
        
        # Adjust event interval based on difficulty
        self.event_interval = random.uniform(
            15.0 / multiplier,  # Events happen more frequently at higher difficulty
            20.0 / multiplier
        )
        
        # Adjust minimum gap between events
        self.min_gap_between_events = max(5.0, 10.0 / multiplier)
        
    def update(self, delta_time):
        try:
            # Update cooldown timer
            if self.cooldown_timer > 0:
                self.cooldown_timer -= delta_time
                return

            # Update existing events
            new_active_events = []
            for event in self.active_events:
                event.time_remaining -= delta_time
                if event.time_remaining > 0:
                    new_active_events.append(event)
                else:
                    logger.debug(f"Event ended: {event.description}")
                    self.cooldown_timer = max(event.cooldown, self.min_gap_between_events)
            self.active_events = new_active_events

            # Generate and handle warnings/events
            if not self.active_events and self.cooldown_timer <= 0:
                self.event_timer += delta_time
                
                if self.event_timer >= self.event_interval - self.warning_time and not self.is_warning:
                    # Start warning phase
                    self.is_warning = True
                    self._generate_pending_event()
                    logger.debug("Warning phase started")
                
                elif self.event_timer >= self.event_interval:
                    # Convert pending event to active event
                    self.event_timer = 0
                    self.event_interval = random.uniform(15.0 / self.difficulty_multiplier, 
                                                       20.0 / self.difficulty_multiplier)
                    self.is_warning = False
                    if self.pending_event:
                        self.active_events.append(self.pending_event)
                        self.events_handled += 1
                        logger.debug(f"Event activated: {self.pending_event.description}")
                        self.pending_event = None
                    
        except Exception as e:
            log_exception(e, "Error in EventSystem update")

    def _generate_pending_event(self):
        """Generate a new pending event with difficulty-adjusted effects."""
        event_data = random.choice(self.possible_events)
        adjusted_effects = {}
        
        # Apply difficulty multiplier to event effects
        for factor, value in event_data["effects"].items():
            adjusted_effects[factor] = value * self.difficulty_multiplier
            
        self.pending_event = Event(
            event_data["description"],
            adjusted_effects
        )
        logger.debug(f"Generated new event: {event_data['description']} with multiplier {self.difficulty_multiplier}")

    def get_warning_message(self):
        """Get the warning message for the pending event."""
        if self.is_warning and self.pending_event:
            return f"WARNING: {self.pending_event.description}"
        return None

    def get_current_effects(self):
        """Return combined effects of all active events."""
        combined_effects = {"temperature": 0, "ph": 0, "salinity": 0}
        # Since we now only have one event at a time, this is simpler
        if self.active_events:
            event = self.active_events[0]
            for factor, change in event.effects.items():
                combined_effects[factor] = change
        return combined_effects 