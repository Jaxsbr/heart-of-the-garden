import random
from core.components.movement_component import MovementComponent
from core.entities.entity import Entity


class CollisionSystem:
    STEERING_FORCE_MULTIPLIER = 0.01

    def apply_steer(self, entity: Entity, dx, dy, delta):
        """Apply a steering force to the entity's position component."""
        position_component = entity.position_component

        # Introduce random variability in the direction
        variability = 0.2  # Adjust variability as needed (0.2 = 20%)
        random_dx = dx * (1 + random.uniform(-variability, variability))
        random_dy = dy * (1 + random.uniform(-variability, variability))

        # Apply the scaled force to the entity's position
        position_component.x += random_dx * delta
        position_component.y += random_dy * delta

    def calculate_opposite_direction(self, bounds1, bounds2):
        """Calculate the direction vector from bounds1 to bounds2."""
        center1 = bounds1.center
        center2 = bounds2.center

        dx = center1[0] - center2[0]
        dy = center1[1] - center2[1]

        # Normalize the direction vector
        magnitude = (dx**2 + dy**2) ** 0.5
        magnitude = magnitude * CollisionSystem.STEERING_FORCE_MULTIPLIER
        if magnitude == 0:
            return 0, 0

        return dx / magnitude, dy / magnitude

    def update(self, delta, entities: list[Entity]):
        non_move_entities = [
            e for e in entities if not e.get_component(MovementComponent)
        ]
        move_entities = [e for e in entities if e.get_component(MovementComponent)]

        for move_entity in move_entities:
            move_bounds = move_entity.position_component.get_bounds()

            # Check collisions with non-moving entities
            for non_move_entity in non_move_entities:
                non_move_entity_bounds = non_move_entity.position_component.get_bounds()

                if move_bounds.colliderect(non_move_entity_bounds):
                    dx, dy = self.calculate_opposite_direction(
                        move_bounds, non_move_entity_bounds
                    )
                    self.apply_steer(move_entity, dx, dy, delta)

            # Check collisions with other moving entities
            for other_entity in move_entities:
                if move_entity is other_entity:
                    continue

                other_bounds = other_entity.position_component.get_bounds()

                if move_bounds.colliderect(other_bounds):
                    dx, dy = self.calculate_opposite_direction(
                        move_bounds, other_bounds
                    )

                    # Apply "half" negative steer to distribute the reaction force
                    self.apply_steer(move_entity, dx * 0.5, dy * 0.5, delta)
