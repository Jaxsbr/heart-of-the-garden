from dataclasses import dataclass, field
from operator import attrgetter
from core.components import Component, MovementComponent, PositionComponent
from core.entities.heart import Heart
from core.entities.plant import Plant
from core.entities.protector import Protector
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes

@dataclass
class EnemyAISystem:
    event_dispatcher: EventDispatcher
    _attackable_entities: list[Protector | Plant | Heart] = field(default_factory=list)


    def update(self, entities, delta):
        self._set_attackable_entities(entities)

        for entity in entities:
            if not self._has_valid_components(entity):
                continue

            movement_component: MovementComponent = entity.movement_component
            if entity.encounter_component.is_fleeing:
            # if movement_component.target_x is not None and movement_component.target_y is not None:
            #     # TODO: Reevaluate if current target is valid (e.g. protect ran off, plant destroyed)
                continue # already have a target

            # Target the heart by default
            highest_priority_attackable = self._get_highest_priority_attackable()
            if highest_priority_attackable is not None:
                # Direct collisions with plant or protector is assigned instead of default heart target
                enemy_entity_bounds = entity.position_component.get_bounds()
                colliding_target_entity = self._get_attackable_collision_entity(enemy_entity_bounds)

                if colliding_target_entity is not None: # in and encounter already
                    self._notify_encounter(entity, colliding_target_entity)
                    # self._set_move_target(movement_component, colliding_target_entity.position_component) # TODO: remove, handle in encounter_system/ new function here
                else: # no encounter, move to the heart
                    self._set_move_target(movement_component, highest_priority_attackable.position_component)


    def _set_attackable_entities(self, entities):
        self._attackable_entities = [entity for entity in entities if hasattr(entity, Component.ATTACKABLE)]
        self._attackable_entities.sort(key=attrgetter('attackable_component.attack_priority'), reverse=True)


    def _has_valid_components(self, entity) -> bool:
        return (hasattr(entity, Component.ENEMY_AI))


    def _get_highest_priority_attackable(self):
        if len(self._attackable_entities) <= 0:
            return None

        highest_priority_attackable = self._attackable_entities[0] # Sorted
        return highest_priority_attackable


    def _get_attackable_collision_entity(self, enemy_entity_bounds):
        # TODO: put all collisions in a list
        # Rank and return top one:
        # 1. Already in ecounter
        # 2. Attack priority

        for attackable in self._attackable_entities:
            if attackable.position_component.intersects(enemy_entity_bounds):
                return attackable # This attackable is colliding with the enemy entity
        return None # None of attack_priority type collided


    def _notify_encounter(self, enemy_entity, attackable_entity):
        encounter_started_event = EventTypes.EncounterStartedEvent(
            enemy_entity=enemy_entity,
            attackable_entity=attackable_entity
        )
        self.event_dispatcher.dispatch(BaseEvent(
            EventTypes.ECOUNTER_STARTED, encounter_started_event))


    def _set_move_target(self, movement_component: MovementComponent, target_position_component: PositionComponent):
        target_center = target_position_component.get_center()
        movement_component.target_x = target_center[0]
        movement_component.target_y = target_center[1]
