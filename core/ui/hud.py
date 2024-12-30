import pygame


class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, heart):
        # Display the Heart's health
        health_text = f"Heart Health: {heart.health}"
        health_surface = self.font.render(health_text, True, (255, 255, 255))
        self.screen.blit(health_surface, (10, 10))

        # Display the wave information
        wave_text = "Wave: 1"  # Fixed wave number for MVP
        wave_surface = self.font.render(wave_text, True, (255, 255, 255))
        self.screen.blit(wave_surface, (10, 40))
