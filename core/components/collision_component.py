from dataclasses import dataclass
from core.components.component import Component


@dataclass
class CollisionComponent(Component):
    weight: float
