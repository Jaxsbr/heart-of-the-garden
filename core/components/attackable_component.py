from dataclasses import dataclass

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent


@dataclass
class AttackableComponent(Component):
    attack_priority: int
