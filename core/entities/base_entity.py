from dataclasses import dataclass, field
import uuid

from core.components import DirectionComponent, EncounterComponent, PositionComponent, SelectionComponent, SpriteComponent, VelocityComponent


@dataclass
class BaseEntity():
    position_component: PositionComponent
    sprite_component: SpriteComponent
    velocity_component: VelocityComponent = field(init=False)
    direction_component: DirectionComponent = field(init=False)
    selection_component: SelectionComponent = field(init=False)
    encounter_component: EncounterComponent = field(init=False)
    entity_id: str = field(init=False)

    def __post_init__(self):
        self.entity_id = str(uuid.uuid4())
        self.velocity_component = VelocityComponent()
        self.direction_component = DirectionComponent()
        self.selection_component = SelectionComponent()
        self.encounter_component = EncounterComponent()
