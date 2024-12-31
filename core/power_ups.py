import random
import pygame
import config

class PowerUp:
    def __init__(self, name, description, duration, effect):
        self.name = name
        self.description = description
        self.duration = duration
        self.effect = effect
        self.active = False
        self.time_remaining = 0
        
    def activate(self):
        self.active = True
        self.time_remaining = self.duration
        
    def update(self, delta_time):
        if self.active:
            self.time_remaining -= delta_time
            if self.time_remaining <= 0:
                self.active = False
                return True
        return False

class PowerUpManager:
    def __init__(self, screen, game_manager):
        self.screen = screen
        self.game_manager = game_manager
        self.font = pygame.font.Font(None, 28)
        self.power_ups = self.create_power_ups()
        self.time_until_next = random.uniform(20, 40)
        
    def create_power_ups(self):
        return [
            PowerUp(
                "Stabilizer",
                "Reduces environmental fluctuations",
                15.0,
                lambda gm: setattr(gm, "damage_multiplier", 0.5)
            ),
            PowerUp(
                "Rapid Recovery",
                "Doubles health regeneration",
                10.0,
                lambda gm: setattr(gm.health_system, "regen_rate", 2.0)
            ),
            PowerUp(
                "Event Shield",
                "Blocks the next negative event",
                20.0,
                lambda gm: setattr(gm.event_system, "event_blocked", True)
            )
        ]
        
    def update(self, delta_time):
        # Update active power-ups
        for power_up in self.power_ups:
            if power_up.update(delta_time):
                # Reset effect when power-up expires
                power_up.effect(self.game_manager)
                
        # Check for new power-up spawn
        self.time_until_next -= delta_time
        if self.time_until_next <= 0:
            self.spawn_random_power_up()
            self.time_until_next = random.uniform(20, 40)
            
    def spawn_random_power_up(self):
        available = [p for p in self.power_ups if not p.active]
        if available:
            power_up = random.choice(available)
            # Create visual notification
            return power_up
            
    def draw(self):
        x = 20
        y = config.SCREEN_HEIGHT - 100
        
        for power_up in self.power_ups:
            if power_up.active:
                # Draw power-up status
                text = f"{power_up.name}: {power_up.time_remaining:.1f}s"
                surface = self.font.render(text, True, config.WHITE)
                self.screen.blit(surface, (x, y))
                y += 30 