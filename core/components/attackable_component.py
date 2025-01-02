from dataclasses import dataclass

from core.components.component import Component


@dataclass
class AttackableComponent(Component):
    attack_priority: int
