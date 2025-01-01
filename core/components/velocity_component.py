from dataclasses import dataclass, field

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent


@dataclass
class VelocityComponent(LivingEntityComponent):
    x: float = field(default=0)
    y: float = field(default=0)
