from dataclasses import dataclass, field
from typing import Any
import uuid

from core.eventing.base_event import BaseEvent


@dataclass
class EventDispatcher:
    listeners: dict[str, Any] = field(default_factory=dict)

    def register_listener(self, listener, key: str):
        self.listeners[key] = listener


    def deregister_listener(self, listener, key: str):
        del self.listeners[key]


    def dispatch(self, event: BaseEvent):
        if event.id == "":
            event.id = str(uuid.uuid4())
        for key, listener in self.listeners.items():
            handled = listener.on_event(event)
            if handled:
                print(f"{key}: {event.id} EVENT: {event.event_name}")
