from core.components import AttackableComponent
from core.entities.base_entity import BaseEntity

class Plant(BaseEntity):
    attackable_component: AttackableComponent

    def __post_init__(self):
        super().__post_init__()
