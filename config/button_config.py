import pygame

class ButtonConfig:
    def __init__(self, font_size, hover_color, text_color, back_color, button_size, border_thickness, click_tick) -> None:
        self.font_size = font_size
        self.font = pygame.font.Font(
            pygame.font.get_default_font(),
            font_size)
        self.hover_color = hover_color
        self.text_color = text_color
        self.back_color = back_color
        self.button_size = button_size
        self.border_thickness = border_thickness
        self.click_tick = click_tick


def get_default_button_config():
    return ButtonConfig(
        font_size=36,
        hover_color="cornflowerblue",
        text_color="darkgray",
        back_color="gray",
        button_size=(250, 75),
        border_thickness=4,
        click_tick=0.2)
