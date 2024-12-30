import pygame


class Button:
    def __init__(self, position, text, button_config, click_action):
        self.text = text
        self._button_config = button_config
        self.click_action = click_action

        self.rect = pygame.Rect(
            position[0],
            position[1],
            button_config.button_size[0],
            button_config.button_size[1],
        )

        self.is_hover = False
        self.is_clicked = False
        self.click_tick = self._button_config.click_tick
        self.click_elapsed = 0

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        self.is_hover = False
        if self.rect.collidepoint(mouse_pos):
            self.is_hover = True
            if mouse_clicked and not self.is_clicked:
                self.is_clicked = True
                self.click_action()

        if self.is_clicked:
            self.click_elapsed += dt * 1
            if self.click_elapsed >= self.click_tick:
                self.is_clicked = False
                self.click_elapsed = 0

    def draw(self, screen):
        config = self._button_config
        pygame.Surface.fill(screen, config.back_color, self.rect)
        color = config.hover_color if self.is_hover else config.text_color
        pygame.draw.rect(screen, color, self.rect, config.border_thickness)
        text_surface = config.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=(self.rect.center))
        screen.blit(text_surface, text_rect)
