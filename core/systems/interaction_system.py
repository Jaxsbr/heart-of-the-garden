from dataclasses import dataclass, field
from core.components.retreat_component import RetreatComponent
from core.components.interaction_component import InteractionComponent
from core.entities.entity import Entity
from core.entities.identifier import is_heart_entity, is_protector_entity
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes
from core.interaction_session import InteractionSession


@dataclass
class InteractionManager:
    interactions: dict[str, InteractionSession] = field(default_factory=dict)

    def register_interaction(self, initiator: Entity, target: Entity):
        key = f"{initiator.entity_id}_{target.entity_id}"
        for key in self.interactions.keys():
            if key.startswith(initiator.entity_id) or key.startswith(target.entity_id):
                return  # One of the entities is already in an interaction
        self.interactions[key] = InteractionSession(initiator, target)

    def process_interaction(self, interaction: InteractionSession, max_points: int):
        initiator, target = interaction.initiator, interaction.target

        initiator_interaction_component = initiator.get_component(InteractionComponent)
        initiator_retreat_component = initiator.get_component(RetreatComponent)
        target_interaction_component = target.get_component(InteractionComponent)

        if (
            initiator_interaction_component is None
            or initiator_retreat_component is None
            or target_interaction_component is None
        ):
            return False

        if is_heart_entity(target):
            # Heart interaction duration reduces health (e.g. enemy attacking)
            target_interaction_component.interaction_duration += 1

        if is_protector_entity(target):
            target_interaction_component.interaction_duration += 5
            initiator_interaction_component.interaction_duration += 100

        # Evaluate interaction outcomes
        if initiator_interaction_component.interaction_duration >= max_points:
            initiator_retreat_component.is_retreating = True
            initiator_interaction_component.interaction_duration = 0
            return True  # Interaction ends
        return False  # Interaction continues


@dataclass
class InteractionSystem:
    event_dispatcher: EventDispatcher
    interaction_manager: InteractionManager = field(default_factory=InteractionManager)

    def __post_init__(self):
        self.event_dispatcher.register_listener(self)

    def on_event(self, event: BaseEvent):
        if event.event_name == EventTypes.INTERACTION_STARTED:
            data = event.event_data
            if data is not None:
                self.interaction_manager.register_interaction(
                    data.initiator, data.target
                )
                return True
        return False

    def update(self):
        completed_interactions = []
        for key, interaction in self.interaction_manager.interactions.items():
            if self.interaction_manager.process_interaction(
                interaction, max_points=200
            ):
                completed_interactions.append(key)

        for key in completed_interactions:
            del self.interaction_manager.interactions[key]
