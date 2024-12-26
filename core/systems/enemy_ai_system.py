from dataclasses import dataclass, field
from operator import attrgetter
from core.components import Component, MovementComponent, PositionComponent
from core.entities.base_entity import BaseEntity

@dataclass
class EnemyAISystem:
    _attackable_entities: list[BaseEntity] = field(default_factory=list)

    def update(self, entities, delta):
        self._set_attackable_entities(entities)

        for entity in entities:
            if not self._has_valid_components(entity):
                continue

            movement_component: MovementComponent = entity.movement_component
            self._set_priority_attack_target(movement_component)


    def _set_priority_attack_target(self, movement_component: MovementComponent):
        if movement_component.target_x is not None and movement_component.target_y is not None:
            return # already have a target

        hpa_position_component = self._get_highest_priority_attackable_pos()
        if hpa_position_component is not None:
            target_center = hpa_position_component.get_center()
            movement_component.target_x = target_center[0]
            movement_component.target_y = target_center[1]


    def _get_highest_priority_attackable_pos(self):
        if len(self._attackable_entities) <= 0:
            return None

        highest_priority_attackable = self._attackable_entities[0] # Sorted
        return highest_priority_attackable.position_component


    def _set_attackable_entities(self, entities):
        self._attackable_entities = [entity for entity in entities if hasattr(entity, Component.ATTACKABLE)]
        self._attackable_entities.sort(key=attrgetter('attackable_component.attack_priority'), reverse=True)


    def _has_valid_components(self, entity) -> bool:
        return (hasattr(entity, Component.ENEMY_AI))
