from dataclasses import dataclass
from core.entities.entity import Entity


class EventTypes:
    SELECTION_CHANGED = "selection_changed"
    ECOUNTER_STARTED = "encounter_started"

    @dataclass
    class EncounterStartedEvent:
        enemy_entity: Entity
        attackable_entity: Entity
