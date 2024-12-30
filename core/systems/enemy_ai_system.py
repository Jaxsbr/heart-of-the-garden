from dataclasses import dataclass, field
from core.attack_priority import AttackPriority
from core.components.attackable_component import AttackableComponent
from core.components.encounter_component import EncounterComponent
from core.components.enemy_ai_component import EnemyAIComponent
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

        for entity in entities:
            enemy_ai_component = entity.get_component(EnemyAIComponent)
            movement_component = entity.get_component(MovementComponent)
            encounter_component = entity.get_component(EncounterComponent)
            if (
                enemy_ai_component is None
                or movement_component is None
                or encounter_component is None
            ):
                continue

            if encounter_component.is_fleeing:
                # The enemy is fleeing, prevent any target/encounter calculations
                continue

            # Target the heart by default
            highest_priority_attackable = self._get_highest_priority_attackable()
            if highest_priority_attackable is not None:
                # Direct collisions with plant or protector is assigned instead of default heart target
                enemy_entity_bounds = entity.position_component.get_bounds()
                colliding_target_entity = self._get_attackable_collision_entity(
                    enemy_entity_bounds
                )

                if colliding_target_entity is not None:
                    # in an encounter already
                    self._notify_encounter(entity, colliding_target_entity)
                else:
                    # no encounter, move to the heart
                    self._set_move_target(
                        movement_component,
                        highest_priority_attackable.position_component,
                    )

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

    def _get_highest_priority_attackable(self):
        if len(self._attackable_entities) <= 0:
            return None

        highest_priority_attackable = self._attackable_entities[0]  # Sorted
        return highest_priority_attackable

    def _get_attackable_collision_entity(self, enemy_entity_bounds):
        # TODO: put all collisions in a list
        # Rank and return top one:
        # We only want to fight the current encounter target
        # 1. Already in encounter
        # 2. Attack priority

        for attackable in self._attackable_entities:
            if attackable.position_component.intersects(enemy_entity_bounds):
                return attackable  # This attackable is colliding with the enemy entity
        return None  # None of attack_priority type collided

    def _notify_encounter(self, enemy_entity, attackable_entity):
        encounter_started_event = EventTypes.EncounterStartedEvent(
            enemy_entity=enemy_entity, attackable_entity=attackable_entity
        )
        self.event_dispatcher.dispatch(
            BaseEvent(EventTypes.ECOUNTER_STARTED, encounter_started_event)
        )

    def _set_move_target(
        self,
        movement_component: MovementComponent,
        target_position_component: PositionComponent,
    ):
        target_center = target_position_component.get_center()
        movement_component.target_x = target_center[0]
        movement_component.target_y = target_center[1]
