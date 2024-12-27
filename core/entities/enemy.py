from dataclasses import dataclass

from core.components import DirectionalRotationComponent, EnemyAIComponent, MovementComponent
from core.entities.base_entity import BaseEntity

@dataclass
class Enemy(BaseEntity):
    movement_component: MovementComponent
    directional_rotation_component: DirectionalRotationComponent
    enemy_ai_component: EnemyAIComponent

    def __post_init__(self):
        super().__post_init__()
