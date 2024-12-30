from dataclasses import dataclass, field

from core.components.component import Component


@dataclass
class EncounterComponent(Component):
    encounter_points: int = field(default=0)
    max_encounter_points_reached: bool = field(default=False)
    is_fleeing: bool = field(default=False)
    flee_tick: float = field(default=10)
    flee_elapsed: float = field(default=0)
