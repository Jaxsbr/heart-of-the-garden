from dataclasses import dataclass, field
from typing import Any

@dataclass
class BaseEvent():
    event_name: str
    event_data: Any | None = field(default=None)
    id: str = field(default="")
