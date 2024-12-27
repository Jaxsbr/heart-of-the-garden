from dataclasses import dataclass, field
from core.components import AttackableComponent, ControllableComponent, DirectionalRotationComponent, MovementComponent
from core.entities.base_entity import BaseEntity


@dataclass
class Protector(BaseEntity):
    movement_component: MovementComponent
    directional_rotation_component: DirectionalRotationComponent
    attackable_component: AttackableComponent
    controllable_component: ControllableComponent = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.controllable_component = ControllableComponent()
