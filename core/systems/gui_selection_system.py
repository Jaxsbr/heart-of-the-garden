from dataclasses import dataclass, field

import pygame
from core.components.gui_selection_component import GUISelectionComponent
from core.entities.entity import Entity
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes
from core.ui.gui_types import GUITypes


@dataclass
class GUISelectionSystem:
    event_dispatcher: EventDispatcher
    current_selected_gui_type: GUITypes | None = field(default=None)

    def __post_init__(self):
        self.event_dispatcher.register_listener(self)

    def on_event(self, event: BaseEvent):
        if (
            event.event_name == EventTypes.GUI_BUTTON_SELECTED
            and event.event_data is not None
        ):
            gui_button_selected_event: EventTypes.GUIButtonSelectedEvent = (
                event.event_data
            )
            button_action = gui_button_selected_event.action
            self.current_selected_gui_type = GUITypes(button_action)
            print(f"event detected: {button_action}")
            return True
        return False

    def update(self, entities: list[Entity]):
        for entity in entities:
            gui_selection_component = entity.get_component(GUISelectionComponent)
            if gui_selection_component is None:
                continue

            if (
                self.current_selected_gui_type is not None
                and gui_selection_component.gui_type == self.current_selected_gui_type
            ):
                gui_selection_component.is_selected = True

            else:
                gui_selection_component.is_selected = False

    def render(self, screen: pygame.Surface):
        if (
            self.current_selected_gui_type is not None
            and self.current_selected_gui_type == GUITypes.ACTION_BUTTONS
        ):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pygame.draw.rect(screen, "green", pygame.Rect(mouse_x, mouse_y, 25, 25))
