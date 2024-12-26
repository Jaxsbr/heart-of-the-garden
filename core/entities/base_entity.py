from dataclasses import dataclass, field

from core.components import DirectionComponent, PositionComponent, SelectionComponent, SpriteComponent, VelocityComponent


@dataclass
class BaseEntity():
    position_component: PositionComponent
    sprite_component: SpriteComponent
    velocity_component: VelocityComponent = field(init=False)
    direction_component: DirectionComponent = field(init=False)
    selection_component: SelectionComponent = field(init=False)

    def __post_init__(self):
        self.velocity_component = VelocityComponent()
        self.direction_component = DirectionComponent()
        self.selection_component = SelectionComponent()
