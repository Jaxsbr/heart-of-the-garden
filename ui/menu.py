from typing import Callable
from menu.button_config import get_default_button_config
from menu.menu_config import get_default_menu_config
from enums import GameState
from menu.button import Button
from state_manager import StateManager
from state import State
import pygame

class Menu(State):
    def __init__(self, bounds: pygame.Rect, state_manager: StateManager):
        self._bounds = bounds
        self._state_manager = state_manager
        self._buttons = []

        buttons: dict[str, Callable[[], None]] = {
            "Play": self._go_to_game,
            "Exit": exit
        }

        menu_config = get_default_menu_config()
        button_config = get_default_button_config()
        y_pos = menu_config.layout_position[1]
        for k, v in buttons.items():
            self._buttons.append(Button(
                position=(menu_config.layout_position[0], y_pos),
                text=k,
                button_config=button_config,
                click_action=v))
            y_pos += button_config.button_size[1] + menu_config.button_offset[1]

    def update(self, dt):
        for button in self._buttons:
            button.update(dt)

    def draw(self, screen):
        screen.fill("gray")
        for button in self._buttons:
            button.draw(screen)

    def _go_to_game(self):
        self._state_manager.change(GameState.GAME)
