import pygame
import config

class Achievement:
    def __init__(self, name, description, condition):
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = False
        self.notification_time = 3.0
        self.time_remaining = 0
        
    def check(self, game_state):
        if not self.unlocked and self.condition(game_state):
            self.unlocked = True
            self.time_remaining = self.notification_time
            return True
        return False

class AchievementManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.achievements = self.create_achievements()
        
    def create_achievements(self):
        return [
            Achievement(
                "Perfect Balance",
                "Maintain optimal conditions for 30 seconds",
                lambda state: state.get("optimal_time", 0) >= 30
            ),
            Achievement(
                "Quick Recovery",
                "Restore reef health from below 30% to above 70%",
                lambda state: state.get("recovery_achieved", False)
            ),
            Achievement(
                "Event Master",
                "Successfully handle 5 consecutive events",
                lambda state: state.get("events_handled", 0) >= 5
            )
        ]
        
    def update(self, delta_time, game_state):
        for achievement in self.achievements:
            if achievement.time_remaining > 0:
                achievement.time_remaining -= delta_time
                
    def check_achievements(self, game_state):
        for achievement in self.achievements:
            achievement.check(game_state)
            
    def draw(self):
        y = 50
        for achievement in self.achievements:
            if achievement.time_remaining > 0:
                # Draw achievement notification
                text = f"Achievement Unlocked: {achievement.name}"
                surface = self.font.render(text, True, config.GREEN)
                rect = surface.get_rect(right=config.SCREEN_WIDTH - 20, top=y)
                
                # Draw background
                bg_rect = rect.inflate(20, 10)
                pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
                pygame.draw.rect(self.screen, config.GREEN, bg_rect, 2)
                
                self.screen.blit(surface, rect)
                y += 50 