from dataclasses import dataclass
from core.entities.enemy import Enemy
from core.entities.heart import Heart
from core.entities.plant import Plant
from core.entities.protector import Protector


class EventTypes():
    SELECTION_CHANGED = "selection_changed"
    ECOUNTER_STARTED = "encounter_started"

    @dataclass
    class EncounterStartedEvent:
        enemy_entity: Enemy
        attackable_entity: Protector | Plant | Heart
