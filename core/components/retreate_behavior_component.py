from dataclasses import dataclass, field

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent
from core.retreat_move_types import RetreatMoveTypes


@dataclass
class RetreatBehaviorComponent(Component):
    move_type: RetreatMoveTypes
    retreat_in_progress: bool = field(default=False)
    retreat_target_x: float | None = field(default=None)
    retreat_target_y: float | None = field(default=None)
    retreat_direction: tuple = field(default=(0, 0))  # Direction vector (x, y)
    tick: float = field(default=2)
    elapsed: float = field(default=0)

    def get_retreat_target(self):
        if self.retreat_target_x is not None and self.retreat_target_y is not None:
            return self.retreat_target_x, self.retreat_target_y
        return None

    def set_retreat_target(self, target):
        self.retreat_target_x, self.retreat_target_y = target
