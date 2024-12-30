from typing import Dict, Type, TypeVar, Optional, cast
import uuid

from core.components.component import Component
from core.components.direction_component import DirectionComponent
from core.components.living_entity_component import LivingEntityComponent
from core.components.position_component import PositionComponent
from core.components.sprite_component import SpriteComponent
from core.components.velocity_component import VelocityComponent
from core.entities.base_entity import BaseEntity

T = TypeVar("T", bound="Component")


class Entity(BaseEntity):
    def __init__(
        self,
        position_component: PositionComponent,
        sprite_component: SpriteComponent,
        velocity_component: VelocityComponent,
        direction_component: DirectionComponent,
    ):
        self._position = position_component
        self._sprite = sprite_component
        self._velocity = velocity_component
        self._direction = direction_component
        self.components: Dict[Type[Component], Component] = {}
        self.entity_id: str = str(uuid.uuid4())

    @property
    def position_component(self) -> PositionComponent:
        return self._position

    @property
    def sprite_component(self) -> SpriteComponent:
        return self._sprite

    @property
    def velocity_component(self) -> VelocityComponent:
        return self._velocity

    @property
    def direction_component(self) -> DirectionComponent:
        return self._direction

    def add_component(self, component: Component):
        self.components[type(component)] = component

    def get_component(self, component_type: Type[T]) -> Optional[T]:
        self._valid_component(component_type)
        component = self.components.get(component_type)  # Type-safe access
        return cast(Optional[T], component)

    def has_component(self, component_type: Type[Component]) -> bool:
        return component_type in self.components

    def _valid_component(self, component_type: Type[Component]):
        if issubclass(component_type, LivingEntityComponent):
            raise KeyError(f"{component_type.__name__} must be accessed directly")
