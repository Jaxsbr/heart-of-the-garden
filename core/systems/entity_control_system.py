from dataclasses import dataclass, field
import pygame

from core.components.controllable_component import ControllableComponent
from core.components.movement_component import MovementComponent
from core.entities.entity import Entity
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes


@dataclass
class EntityControlSystem:
    event_dispatcher: EventDispatcher
    selection_elapsed: float = field(default=0)
    selection_tick: float = field(default=0.2)

    # selecting, indicates we just changes selection and want to ensure the
    # mouse action completes and does not immediately set a target where the
    # entity was just selected
    selecting: bool = field(default=False)

    target_set_elapsed: float = field(default=0)
    target_set_tick: float = field(default=0.2)
    target_setting: bool = field(default=False)

    def __post_init__(self):
        self.event_dispatcher.register_listener(self)

    def on_event(self, event: BaseEvent) -> bool:
        if event.event_name == EventTypes.SELECTION_CHANGED:
            self.selecting = True
            return True
        return False

    def update(self, delta, entities: list[Entity], screen_offset):
        self._update_selection_timing(delta)
        self._update_target_setting_timing(delta)
        self._update_movement_target(entities, screen_offset)

    def _update_selection_timing(self, delta):
        if self.selection_elapsed >= self.selection_tick:
            self.selection_elapsed = 0
            self.selecting = False

        if self.selecting:
            self.selection_elapsed += delta * 1

    def _update_target_setting_timing(self, delta):
        if self.target_set_elapsed >= self.target_set_tick:
            self.target_set_elapsed = 0
            self.target_setting = False

        if self.target_setting:
            self.target_set_elapsed += delta * 1

    def _update_movement_target(self, entities: list[Entity], screen_offset):
        if self.selecting or self.target_setting:
            return

        for entity in entities:
            movement_component = entity.get_component(MovementComponent)
            controllable_component = entity.get_component(ControllableComponent)
            if movement_component is None or controllable_component is None:
                continue

            # ATM we assume this is the Protector due to controllable component
            mouse_clicked = pygame.mouse.get_pressed()[0]
            if mouse_clicked:  # and entity.selection_component.is_selected:
                self.target_setting = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                movement_component.target_x = mouse_x - screen_offset[0]
                movement_component.target_y = mouse_y - screen_offset[1]
