import json
import random
import os

"""
Facts Manager Module

Manages educational facts about coral reefs that are displayed during gameplay.
Provides relevant information based on game events and coral health status.

Features:
- Fact rotation system
- Context-sensitive fact selection
- Timed display management
- Educational content integration
"""

class FactsManager:
    def __init__(self):
        self.facts = self.load_facts()
        self.current_fact = None
        self.display_time = 5.0  # How long to show each fact
        self.time_until_next = 30.0  # Time between facts
        
    def load_facts(self):
        try:
            with open(os.path.join("assets", "facts.json"), "r") as f:
                return json.load(f)
        except:
            print("Warning: Could not load facts file")
            return {
                "temperature": [
                    "Coral reefs thrive in water temperatures between 23-29°C (73-84°F).",
                    "Temperature changes of just 1-2°C can cause coral bleaching."
                ],
                "ph": [
                    "Ocean acidification makes it harder for corals to build their skeletons.",
                    "The ocean's pH has dropped by 0.1 units since the industrial revolution."
                ],
                "salinity": [
                    "Most coral reefs need a salinity level between 32-42 parts per thousand.",
                    "Heavy rains can temporarily lower salinity near coastal reefs."
                ]
            }
            
    def update(self, delta_time):
        self.time_until_next -= delta_time
        
        if self.time_until_next <= 0:
            self.select_new_fact()
            self.time_until_next = 30.0
            
    def select_new_fact(self):
        # Choose a category based on current conditions
        categories = list(self.facts.keys())
        category = random.choice(categories)
        self.current_fact = random.choice(self.facts[category])
        
    def get_current_fact(self):
        return self.current_fact 