from dataclasses import dataclass, field

from core.components.component import Component
from core.direction import Direction


@dataclass
class DirectionalRotationComponent(Component):
    direction: Direction
    degrees: float = field(default=0)
    rotation_speed: float = field(default=5)
