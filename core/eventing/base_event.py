from dataclasses import dataclass, field
from typing import Any

@dataclass
class BaseEvent():
    event_name: str
    args: dict[str, Any] = field(default_factory=dict)
    id: str = field(default="")
