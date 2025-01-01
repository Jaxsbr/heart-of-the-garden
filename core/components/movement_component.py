from dataclasses import dataclass, field

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent


@dataclass
class MovementComponent(Component):
    speed: float
    min_speed: float
    acceleration_rate: float
    deceleration_rate: float
    slow_down_distance: float
    target_reach_distance: float
    steering_force: float
    current_speed: float = field(default=0)
    target_x: float | None = field(default=None)
    target_y: float | None = field(default=None)
    target_normalized_x: float | None = field(default=None)
    target_normalized_y: float | None = field(default=None)
    distance_to_target: float | None = field(default=None)
