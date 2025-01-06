from dataclasses import dataclass, field
import pygame

from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes
from core.ui.gui_types import GUITypes


@dataclass
class HUD:
    event_dispatcher: EventDispatcher
    screen_size: tuple[int, int]
    gui_bar_image: pygame.Surface
    gui_buttons_image_sprite: pygame.Surface
    font: pygame.font.Font = field(init=False)
    gui_bar_rect: pygame.Rect = field(init=False)
    gui_buttons_rect: pygame.Rect = field(init=False)

    def __post_init__(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

        gui_bar_width = 750
        gui_bar_height = 125

        self.gui_bar_rect = pygame.Rect(
            self.screen_size[0] / 2 - gui_bar_width / 2,
            self.screen_size[1] - gui_bar_height,
            gui_bar_width,
            gui_bar_height,
        )

        gui_buttons_width = 256
        gui_buttons_height = 128

        self.gui_buttons_rect = pygame.Rect(
            self.screen_size[0] - gui_buttons_width,
            self.screen_size[1] - gui_buttons_height,
            gui_buttons_width,
            gui_buttons_height,
        )

    def update(self):
        mouse_clicked = pygame.mouse.get_pressed()[0]
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_clicked and self.gui_buttons_rect.collidepoint((mouse_x, mouse_y)):
            self.event_dispatcher.dispatch(
                BaseEvent(
                    EventTypes.GUI_BUTTON_SELECTED,
                    EventTypes.GUIButtonSelectedEvent(GUITypes.ACTION_BUTTONS),
                )
            )

    def render(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, "gray", self.gui_bar_rect)

        # screen.blit(self.gui_bar_image, (self.gui_bar_rect.x, self.gui_bar_rect.y))
        screen.blit(
            self.gui_buttons_image_sprite,
            (self.gui_buttons_rect.x, self.gui_buttons_rect.y),
        )
