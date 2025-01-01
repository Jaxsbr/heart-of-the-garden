from dataclasses import dataclass, field

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent


@dataclass
class InteractionComponent(Component):
    interaction_duration: int = field(default=0)
