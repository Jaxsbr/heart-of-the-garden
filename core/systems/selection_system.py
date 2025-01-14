from dataclasses import dataclass, field
import pygame

from core.components.selection_component import SelectionComponent
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes
from core.entities.entity import Entity


@dataclass
class SelectionSystem:
    event_dispatcher: EventDispatcher
    selection_elapsed: float = field(default=0)
    selection_tick: float = field(default=0.2)
    selecting: bool = field(default=False)

    def update(self, delta, entities: list[Entity]):
        self._update_selection_timing(delta)

        if self.selecting:
            return

        mouse_clicks = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        selection_changed = False
        for entity in entities:
            selection_occurred = self._update_selection(entity, mouse_clicks, mouse_pos)
            selection_changed = True if selection_occurred else selection_changed

        if selection_changed:
            self.event_dispatcher.dispatch(BaseEvent(EventTypes.SELECTION_CHANGED))
            self.selecting = True

    def _update_selection(self, entity: Entity, mouse_clicks, mouse_pos):
        selection_component = entity.get_component(SelectionComponent)
        if not selection_component:
            return

        mouse_left_clicked = mouse_clicks[0]
        mouse_right_clicked = mouse_clicks[2]

        if mouse_left_clicked:
            # Select the entity that was clicked
            in_bounds = entity.position_component.contains_point(
                (mouse_pos[0], mouse_pos[1])
            )
            within_range = entity.position_component.within_center_distance(
                64, (mouse_pos[0], mouse_pos[1])
            )
            if in_bounds or within_range:
                selection_component.is_selected = True
                return True
        elif mouse_right_clicked:  # Deselected
            selection_component.is_selected = False
            return True
        return False

    def _update_selection_timing(self, delta):
        if self.selection_elapsed >= self.selection_tick:
            self.selection_elapsed = 0
            self.selecting = False

        if self.selecting:
            self.selection_elapsed += delta * 1
