from dataclasses import dataclass, field

from core.components.component import Component


@dataclass
class RetreatComponent(Component):
    is_retreating: bool = field(default=False)
    retreat_tick: float = field(default=10)
    retreat_elapsed: float = field(default=0)
