from dataclasses import dataclass

from core.entities.entity import Entity


@dataclass
class InteractionSession:
    initiator: Entity
    target: Entity
