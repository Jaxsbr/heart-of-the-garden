from dataclasses import dataclass
from core.components import DirectionalRotationComponent, MovementComponent
from core.entities.base_entity import BaseEntity


@dataclass
class Protector(BaseEntity):
    movement_component: MovementComponent
    directional_rotation_component: DirectionalRotationComponent
