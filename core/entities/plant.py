import pygame
from config.game_settings import GameSettings

class Plant(pygame.sprite.Sprite):
    def __init__(self, screen, game_settings, position):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 0, 255))  # Simple representation (Blue square)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.health = game_settings.plant_health

    def update(self):
        # Simple update logic for plants (no special abilities yet)
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)
