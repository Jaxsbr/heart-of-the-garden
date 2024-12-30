from dataclasses import dataclass, field

from core.components.component import Component


@dataclass
class SelectionComponent(Component):
    is_selected: bool = field(default=False)
