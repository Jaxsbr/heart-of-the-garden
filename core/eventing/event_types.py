from dataclasses import dataclass
from core.entities.entity import Entity
from core.ui.gui_types import GUITypes


class EventTypes:
    SELECTION_CHANGED = "selection_changed"
    INTERACTION_STARTED = "interaction_started"
    GUI_BUTTON_SELECTED = "gui_button_selected"

    @dataclass
    class InteractionStartedEvent:
        initiator: Entity
        target: Entity

    @dataclass
    class GUIButtonSelectedEvent:
        action: GUITypes
