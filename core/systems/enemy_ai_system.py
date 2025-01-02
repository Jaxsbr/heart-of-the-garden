from dataclasses import dataclass, field
from core.attack_priority import AttackPriority
from core.components.attackable_component import AttackableComponent
from core.components.interaction_component import InteractionComponent
from core.components.enemy_ai_component import EnemyAIComponent
from core.components.retreat_component import RetreatComponent
from core.components.movement_component import MovementComponent
from core.components.position_component import PositionComponent
from core.entities.entity import Entity
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes


@dataclass
class EnemyAISystem:
    event_dispatcher: EventDispatcher
    _attackable_entities: list[Entity] = field(default_factory=list)

    def update(self, entities: list[Entity], delta):
        self._set_attackable_entities(entities)

        for enemy_entity in entities:
            enemy_ai_component = enemy_entity.get_component(EnemyAIComponent)
            movement_component = enemy_entity.get_component(MovementComponent)
            interaction_component = enemy_entity.get_component(InteractionComponent)
            retreat_component = enemy_entity.get_component(RetreatComponent)
            if (
                enemy_ai_component is None
                or movement_component is None
                or interaction_component is None
                or retreat_component is None
            ):
                continue

            if retreat_component.is_retreating:
                # The enemy is retreating, prevent any target/interaction calculations
                continue

            # Target the heart by default
            self._target_heart_position(movement_component)

            # Direct collisions with plant or protector is assigned instead of default heart target
            colliding_target_entity = self._get_attackable_collision_entity(
                enemy_entity
            )

            if colliding_target_entity is not None:
                # potential interaction, colliding
                self._notify_interaction(enemy_entity, colliding_target_entity)

    def _set_attackable_entities(self, entities: list[Entity]):
        self._attackable_entities = []
        for entity in entities:
            attackable_component = entity.get_component(AttackableComponent)
            if attackable_component is None:
                continue

            if attackable_component.attack_priority == AttackPriority.HIGH:
                # Add the highest priority at the top of the list (heart)
                self._attackable_entities.insert(0, entity)
            else:
                self._attackable_entities.append(entity)

    def _target_heart_position(self, movement_component: MovementComponent):
        if len(self._attackable_entities) <= 0:
            return None

        highest_priority_attackable = self._attackable_entities[0]  # Sorted
        if highest_priority_attackable is not None:
            self._set_move_target(
                movement_component,
                highest_priority_attackable.position_component,
            )

    def _get_attackable_collision_entity(self, enemy_entity: Entity):
        # TODO: put all collisions in a list
        # Rank and return top one:
        # We only want to fight the current interaction target
        # 1. Already in interaction
        # 2. Attack priority

        for attackable in self._attackable_entities:
            collide_distance = (
                attackable.position_component.get_inner_radius()
                + enemy_entity.position_component.get_inner_radius()
            )
            distance_between = attackable.position_component.distance_to_center(
                enemy_entity.position_component.get_center()
            )
            if distance_between < collide_distance / 2:
                return attackable  # This attackable is colliding with the enemy entity
        return None  # None of attack_priority type collided

    def _notify_interaction(self, enemy_entity, attackable_entity):
        interaction_started_event = EventTypes.InteractionStartedEvent(
            initiator=enemy_entity, target=attackable_entity
        )
        self.event_dispatcher.dispatch(
            BaseEvent(EventTypes.INTERACTION_STARTED, interaction_started_event)
        )

    def _set_move_target(
        self,
        movement_component: MovementComponent,
        target_position_component: PositionComponent,
    ):
        target_center = target_position_component.get_center()
        movement_component.target_x = target_center[0]
        movement_component.target_y = target_center[1]
