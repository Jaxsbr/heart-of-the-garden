from abc import ABC, abstractmethod

from core.components.direction_component import DirectionComponent
from core.components.position_component import PositionComponent
from core.components.sprite_component import SpriteComponent
from core.components.velocity_component import VelocityComponent

class BaseEntity(ABC):
    @property
    @abstractmethod
    def position_component(self) -> PositionComponent:
        pass

    @property
    @abstractmethod
    def sprite_component(self) -> SpriteComponent:
        pass

    @property
    @abstractmethod
    def velocity_component(self) -> VelocityComponent:
        pass

    @property
    @abstractmethod
    def direction_component(self) -> DirectionComponent:
        pass
