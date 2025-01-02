from dataclasses import dataclass, field

from core.components.component import Component


@dataclass
class InteractionComponent(Component):
    interaction_duration: int = field(default=0)
