from dataclasses import dataclass
from core.entities.entity import Entity


class EventTypes:
    SELECTION_CHANGED = "selection_changed"
    INTERACTION_STARTED = "interaction_started"

    @dataclass
    class InteractionStartedEvent:
        initiator: Entity
        target: Entity
