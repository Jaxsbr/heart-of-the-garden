from dataclasses import dataclass, field

from core.attack_encounter import AttackEncounter
from core.attack_priority import AttackPriority
from core.components.attackable_component import AttackableComponent
from core.components.controllable_component import ControllableComponent
from core.components.encounter_component import EncounterComponent
from core.components.movement_component import MovementComponent
from core.entities.entity import Entity
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes


@dataclass
class EncounterSystem:
    event_dispatcher: EventDispatcher
    _encounters: dict[str, AttackEncounter] = field(
        default_factory=dict[str, AttackEncounter]
    )

    def __post_init__(self):
        self.event_dispatcher.register_listener(self)

    def _set_encounter(self, enemy_entity, attackable_entity):
        # We are either already in an encounter or about to start one
        key = f"{enemy_entity.entity_id}_{attackable_entity.entity_id}"
        for key in self._encounters.keys():
            if key.startswith(enemy_entity.entity_id):
                return  # found the encounter currently in progress

            if attackable_entity.encounter_component.is_fleeing:
                return  # opponent already fleeing

        # No encounters with this enemy in progress, start one
        self._encounters[key] = AttackEncounter(
            enemy_id=enemy_entity.entity_id, attackable_id=attackable_entity.entity_id
        )

    def _get_entity_by_id(self, entity_id, entities: list[Entity]):
        for entity in entities:
            if entity.entity_id == entity_id:
                return entity
        return None

    def _apply_encounter_points(self, entity: Entity, encounter_entity: Entity):
        e1_encounter_component = entity.get_component(EncounterComponent)
        e2_encounter_component = encounter_entity.get_component(EncounterComponent)
        if e1_encounter_component is None or e2_encounter_component is None:
            return

        if not e2_encounter_component.is_fleeing:
            e1_encounter_component.encounter_points += 1

    def _is_encounter_over(self, entity: Entity, max_encounter_points, is_attackable):
        encounter_reached = False
        encounter_component = entity.get_component(EncounterComponent)
        movement_component = entity.get_component(MovementComponent)
        if encounter_component is None or movement_component is None:
            return encounter_reached

        if encounter_component.encounter_points > max_encounter_points:
            encounter_component.is_fleeing = True
            encounter_component.encounter_points = 0
            encounter_reached = True

        # TODO: Flee/Move system to determine target pos
        if encounter_reached and not is_attackable:
            # TODO: Trigger Enemy Flee notification
            movement_component.target_x = -200
            movement_component.target_y = -200
        elif encounter_reached and is_attackable:
            attackable_component = entity.get_component(AttackableComponent)
            if attackable_component is None:
                return encounter_reached
            attack_priority = attackable_component.attack_priority
            if attack_priority == int(AttackPriority.HIGH):
                print("heart killed")
                exit()  # Heart killed, game over
            elif attack_priority == int(AttackPriority.MEDIUM):
                # TODO: remove plant entity
                print("plant killed")
            elif attack_priority == int(AttackPriority.LOW):  # Protector
                print("protector scared")
                print("protector flees")
                encounter_component.is_fleeing = True
                # TODO: Trigger Flee notification
                movement_component.target_x = 64
                movement_component.target_y = 64
            else:
                print(f"attack_priority: {attack_priority}")

        return encounter_reached

    def _cooldown_protector_flee_time(self, delta, entities: list[Entity]):
        for entity in entities:
            controllable_component = entity.get_component(ControllableComponent)
            encounter_component = entity.get_component(EncounterComponent)
            if controllable_component is None or encounter_component is None:
                continue

            if encounter_component.is_fleeing:
                encounter_component.flee_elapsed += delta * 1

            if (
                encounter_component.is_fleeing
                and encounter_component.flee_elapsed > encounter_component.flee_tick
            ):
                encounter_component.flee_elapsed = 0
                encounter_component.is_fleeing = False
                print("protect stopped fleeing")
            return  # Once protector found exit the loop

    def on_event(self, event: BaseEvent):
        if (
            event.event_name == EventTypes.ECOUNTER_STARTED
            and event.event_data is not None
        ):
            encounter_started_event: EventTypes.EncounterStartedEvent = event.event_data
            self._set_encounter(
                encounter_started_event.enemy_entity,
                encounter_started_event.attackable_entity,
            )
            return True
        return False

    def update(self, delta, entities: list[Entity]):
        self._cooldown_protector_flee_time(
            delta, entities
        )  # TODO: Fleeing needs to move to new system

        # NOTE: we loop a copy as we delete encounters from the original dict in this loop
        copy_encounters = dict(self._encounters).items()
        for encounter in copy_encounters:
            enemy_entity_id = encounter[1].enemy_id  # Enemy
            attackable_entity_id = encounter[1].attackable_id  # Attackable
            enemy_entity = self._get_entity_by_id(enemy_entity_id, entities)
            attackable_entity = self._get_entity_by_id(attackable_entity_id, entities)

            if enemy_entity is None or attackable_entity is None:
                print("Entity was None in encounter")
                return

            # Simple counter that indicates how long the encounter has been going on for
            # Only applied when the opponent is not already fleeing
            self._apply_encounter_points(enemy_entity, attackable_entity)
            self._apply_encounter_points(attackable_entity, enemy_entity)

            enemy_max_encounter_reached = self._is_encounter_over(
                enemy_entity, 200, False
            )
            attackable_max_encounter_reached = self._is_encounter_over(
                attackable_entity, 220, True
            )

            key = f"{enemy_entity_id}_{attackable_entity_id}"
            if (
                enemy_max_encounter_reached or attackable_max_encounter_reached
            ) and key in self._encounters.keys():
                print("encouter removed")

                del self._encounters[key]
