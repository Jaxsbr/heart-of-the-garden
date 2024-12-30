
from dataclasses import dataclass, field

from core.components.component import Component


@dataclass
class FleeComponent(Component):
    is_fleeing: bool = field(default=False)
    flee_tick: float = field(default=10)
    flee_elapsed: float = field(default=0)
