import math
import pygame
from core.components.movement_component import MovementComponent
from core.components.retreat_component import RetreatComponent
from core.components.retreate_behavior_component import RetreatBehaviorComponent
from core.entities.entity import Entity
from core.retreat_move_types import RetreatMoveTypes


class RetreatMovementSystem:
    def update(self, delta, entities: list[Entity]):
        for entity in entities:
            retreat_component = entity.get_component(RetreatComponent)
            retreat_behavior_component = entity.get_component(RetreatBehaviorComponent)
            movement_component = entity.get_component(MovementComponent)

            if (
                not retreat_component
                or not retreat_behavior_component
                or not movement_component
                or retreat_behavior_component.move_type != RetreatMoveTypes.WIGGLE
                or not retreat_component.is_retreating
            ):
                continue

            # TODO: implement TTL mechanism on retreating entity
            ttl = 1
            if ttl < 1:
                return

            # TODO: Perform wiggle
            # Perhaps calculate new ,pve target slightly offset from current direction
            # Keep doing this until TTL is <= 0

            if (
                movement_component.target_normalized_x is not None
                and movement_component.target_normalized_y is not None
            ):
                wiggle_offset = self._get_wiggle_offset(
                    movement_component.target_normalized_x,
                    movement_component.target_normalized_y,
                    retreat_behavior_component.elapsed,
                )
                retreat_behavior_component.elapsed += 1
                entity.position_component.x += wiggle_offset.x
                entity.position_component.y += wiggle_offset.y

    def _get_wiggle_offset(self, tx, ty, elapsed):
        # Calculate perpendicular vector for wiggle
        perpendicular = pygame.math.Vector2(-ty, tx)

        # Apply sinusoidal offset for wiggle
        wiggle_magnitude = 0.6  # How far the enemy wiggles
        wiggle_speed = 0.4  # How fast the enemy wiggles
        wiggle_offset = (
            perpendicular * wiggle_magnitude * math.sin(elapsed * wiggle_speed)
        )
        return wiggle_offset
