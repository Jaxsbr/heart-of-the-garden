from dataclasses import dataclass, field

from core.components.component import Component
from core.ui.gui_types import GUITypes


@dataclass
class GUISelectionComponent(Component):
    gui_type: GUITypes
    is_selected: bool = field(default=False)
