from dataclasses import dataclass, field
import random

import pygame
from core.components.movement_component import MovementComponent
from core.components.collision_component import CollisionComponent
from core.entities.entity import Entity
from core.entities.identifier import is_moving_entity


@dataclass
class CollisionSystem:
    steering_force_multiplier: float = field(default=0.01)

    def apply_steer(self, entity: Entity, dx, dy, delta, weight_ratio):
        """Apply a weighted steering force to the entity's position component."""
        position_component = entity.position_component

        # Introduce random variability in the direction
        variability = 0.2  # Adjust variability as needed (0.2 = 20%)
        random_dx = dx * (1 + random.uniform(-variability, variability))
        random_dy = dy * (1 + random.uniform(-variability, variability))

        # Scale the force by weight ratio and delta
        position_component.x += random_dx * delta * weight_ratio
        position_component.y += random_dy * delta * weight_ratio

    def calculate_opposite_direction(self, bounds1, bounds2):
        """Calculate the direction vector from bounds1 to bounds2."""
        center1 = bounds1.center
        center2 = bounds2.center

        dx = center1[0] - center2[0]
        dy = center1[1] - center2[1]

        # Normalize the direction vector
        magnitude = (dx**2 + dy**2) ** 0.5
        magnitude = magnitude * self.steering_force_multiplier
        if magnitude == 0:
            return 0, 0

        return dx / magnitude, dy / magnitude

    def update(self, delta, entities: list[Entity]):
        non_move_entities = [e for e in entities if not is_moving_entity(e)]
        move_entities = [e for e in entities if is_moving_entity(e)]

        for move_entity in move_entities:
            move_collision_component = move_entity.get_component(CollisionComponent)
            if move_collision_component is None:
                continue
            move_weight = move_collision_component.weight
            move_bounds = move_entity.position_component.get_bounds()

            # Check collisions with non-moving entities
            self._update_move_to_non_moving_collision(
                delta, non_move_entities, move_entity, move_weight, move_bounds
            )

            # Check collisions with other moving entities
            self._update_move_to_move_collision(
                delta, move_entities, move_entity, move_weight, move_bounds
            )

    def _update_move_to_move_collision(
        self,
        delta,
        move_entities: list[Entity],
        move_entity: Entity,
        move_weight: float,
        move_bounds: pygame.Rect,
    ):
        for other_entity in move_entities:
            if move_entity is other_entity:
                continue

            other_collision_component = other_entity.get_component(CollisionComponent)
            if other_collision_component is None:
                continue
            other_weight = other_collision_component.weight
            other_bounds = other_entity.position_component.get_bounds()

            if self._colliding(move_entity, other_entity):
                dx, dy = self.calculate_opposite_direction(move_bounds, other_bounds)

                # Calculate weight ratios for both entities
                total_weight = move_weight + other_weight
                weight_ratio_self = other_weight / total_weight
                weight_ratio_other = move_weight / total_weight

                # Apply "half" negative steer to distribute the reaction force
                self.apply_steer(
                    move_entity, dx * 0.5, dy * 0.5, delta, weight_ratio_self
                )
                self.apply_steer(
                    other_entity, -dx * 0.5, -dy * 0.5, delta, weight_ratio_other
                )

    def _update_move_to_non_moving_collision(
        self,
        delta,
        non_move_entities: list[Entity],
        move_entity: Entity,
        move_weight: float,
        move_bounds: pygame.Rect,
    ):
        move_bounds = move_entity.position_component.get_bounds()
        for non_move_entity in non_move_entities:
            non_move_collision_component = non_move_entity.get_component(
                CollisionComponent
            )
            if non_move_collision_component is None:
                continue
            non_move_weight = non_move_collision_component.weight
            non_move_entity_bounds = non_move_entity.position_component.get_bounds()

            if self._colliding(move_entity, non_move_entity):
                dx, dy = self.calculate_opposite_direction(
                    move_bounds, non_move_entity_bounds
                )
                weight_ratio = non_move_weight / (move_weight + non_move_weight)
                self.apply_steer(move_entity, dx, dy, delta, weight_ratio)

    def _colliding(self, e1: Entity, e2: Entity) -> bool:
        collide_distance = (
            e1.position_component.get_inner_radius()
            + e2.position_component.get_inner_radius()
        )
        distance_between = e1.position_component.distance_to_center(
            e2.position_component.get_center()
        )
        return distance_between < collide_distance / 2
