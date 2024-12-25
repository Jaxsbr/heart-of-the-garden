import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, game_settings, heart):
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings
        self.heart = heart
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))  # Simple representation (Yellow square)
        self.rect = self.image.get_rect()
        self.rect.center = (50, 50)  # Start position of the enemy
        self.speed = game_settings.enemy_speed

    def update(self):
        # Move towards the Heart
        if self.rect.centerx < self.heart.rect.centerx:
            self.rect.x += self.speed
        if self.rect.centery < self.heart.rect.centery:
            self.rect.y += self.speed

    def draw(self):
        self.screen.blit(self.image, self.rect)
