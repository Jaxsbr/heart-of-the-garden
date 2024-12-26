from dataclasses import dataclass
from core.components import AttackableComponent
from core.entities.base_entity import BaseEntity


@dataclass
class Heart(BaseEntity):
    attackable_component: AttackableComponent
