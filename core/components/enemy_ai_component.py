from dataclasses import dataclass, field

from core.components.component import Component


@dataclass
class EnemyAIComponent(Component):
    has_attack_target: bool | None = field(default=False)
