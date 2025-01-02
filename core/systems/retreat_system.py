from dataclasses import dataclass
from core.components.movement_component import MovementComponent
from core.components.retreat_component import RetreatComponent
from core.components.retreate_behavior_component import RetreatBehaviorComponent
from core.entities.entity import Entity


@dataclass
class RetreatSystem:
    screen_size: tuple[int, int]

    def update(self, entities: list[Entity]):
        for entity in entities:
            retreat_component = entity.get_component(RetreatComponent)
            retreat_behavior_component = entity.get_component(RetreatBehaviorComponent)
            movement_component = entity.get_component(MovementComponent)

            if (
                not retreat_behavior_component
                or not movement_component
                or not retreat_component
            ):
                continue

            if (
                retreat_component.is_retreating
                and not retreat_behavior_component.retreat_in_progress
                and movement_component.target_normalized_x is not None
                and movement_component.target_normalized_y is not None
            ):
                # TODO: get distance outside of screen
                outside_distance = 2000
                # Reverse direction
                retreat_target = (
                    -movement_component.target_normalized_x * outside_distance,
                    -movement_component.target_normalized_y * outside_distance,
                )
                retreat_behavior_component.set_retreat_target(retreat_target)
                movement_component.target_x = (
                    retreat_behavior_component.retreat_target_x
                )
                movement_component.target_y = (
                    retreat_behavior_component.retreat_target_y
                )
                movement_component.speed = (
                    movement_component.speed * 1.7
                )  # Retreat fast
                retreat_behavior_component.retreat_in_progress = True
