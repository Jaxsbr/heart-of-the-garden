from dataclasses import dataclass, field

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent


@dataclass
class RetreatComponent(Component):
    is_retreating: bool = field(default=False)
    retreat_tick: float = field(default=10)
    retreat_elapsed: float = field(default=0)
