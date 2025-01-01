from dataclasses import dataclass, field

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent


@dataclass
class DirectionComponent(LivingEntityComponent):
    normalized_x: float | None = field(default=None)
    normalized_y: float | None = field(default=None)
