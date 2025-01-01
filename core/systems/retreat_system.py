from dataclasses import dataclass
from core.components.movement_component import MovementComponent
from core.components.retreat_component import RetreatComponent
from core.components.retreate_behavior_component import RetreatBehaviorComponent
from core.entities.entity import Entity
from core.screen_position_helper import get_random_start_pos


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
            ):
                retreat_target = self._calculate_retreat_position(
                    entity, retreat_behavior_component
                )
                retreat_behavior_component.set_retreat_target(retreat_target)
                movement_component.target_x = (
                    retreat_behavior_component.retreat_target_x
                )
                movement_component.target_y = (
                    retreat_behavior_component.retreat_target_y
                )
                retreat_behavior_component.retreat_in_progress = True

    def _calculate_retreat_position(
        self, entity: Entity, retreat_behavior_component: RetreatBehaviorComponent
    ):
        # Example: Move away from the garden heart or towards the edges of the map
        current_position = entity.position_component.get_center()
        retreat_direction = retreat_behavior_component.retreat_direction

        # TODO: target must be out of screen bounds

        # Retreat to a predefined safe position
        retreat_point = get_random_start_pos(self.screen_size)
        # retreat_x = current_position[0] + retreat_direction[0] * 400
        # retreat_y = current_position[1] + retreat_direction[1] * 400

        return retreat_point.x, retreat_point.y
