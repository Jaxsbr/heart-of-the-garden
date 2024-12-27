import math

from core.components import Component, DirectionComponent, MovementComponent, PositionComponent, VelocityComponent


class MovementSystem:
    def update(self, entities, delta):
        for entity in entities:
            if not self._has_valid_components(entity):
                continue

            movement_component: MovementComponent = entity.movement_component
            position_component: PositionComponent = entity.position_component
            direction_component: DirectionComponent = entity.direction_component
            velocity_component: VelocityComponent = entity.velocity_component

            self._calculate_direction(movement_component, position_component, direction_component)
            self._calculate_target_normalized(movement_component, position_component)
            self._apply_steering_force(movement_component, direction_component)
            self._apply_accelerate_and_decelerate(delta, movement_component)
            self._calculate_velocity(delta, movement_component, direction_component, velocity_component)
            self._apply_velocity(position_component, velocity_component)
            self._update_move_target(movement_component, position_component, velocity_component)


    def _has_valid_components(self, entity) -> bool:
        return (
            hasattr(entity, Component.MOVEMENT) and
            hasattr(entity, Component.POSITION) and
            hasattr(entity, Component.DIRECTION) and
            hasattr(entity, Component.VELOCITY))


    def _calculate_direction(self, movement_component: MovementComponent, position_component: PositionComponent, direction_component: DirectionComponent):
        if movement_component.target_x is None or movement_component.target_y is None:
            direction_component.normalized_x = None
            direction_component.normalized_y = None
        else:
            center_pos = position_component.get_center()
            dx = movement_component.target_x - center_pos[0]
            dy = movement_component.target_y - center_pos[1]

            if dx == 0 and dy == 0:
                return (0, 0)  # Avoid division by zero

            magnitude = math.sqrt(dx**2 + dy**2)
            direction_component.normalized_x = dx / magnitude
            direction_component.normalized_y = dy / magnitude


    def _calculate_target_normalized(self, movement_component: MovementComponent, position_component: PositionComponent):
        if movement_component.target_x is None or movement_component.target_y is None:
            return

        center_pos = position_component.get_center()
        target_vector_x = movement_component.target_x - center_pos[0]
        target_vector_y = movement_component.target_y - center_pos[1]
        movement_component.distance_to_target = (target_vector_x**2 + target_vector_y**2)**0.5

        if movement_component.distance_to_target is None:
            return

        if movement_component.distance_to_target != 0:
            movement_component.target_normalized_x = target_vector_x / movement_component.distance_to_target
            movement_component.target_normalized_y = target_vector_y / movement_component.distance_to_target
        else:
            movement_component.target_normalized_x = 0
            movement_component.target_normalized_y = 0


    def _apply_steering_force(self, movement_component: MovementComponent, direction_component: DirectionComponent):
        if (direction_component.normalized_x is None or
            direction_component.normalized_y is None or
            movement_component.target_normalized_x is None or
            movement_component.target_normalized_y is None):
            return

        # Interpolate direction (steering behavior)
        steering_force = movement_component.steering_force
        new_dx = (1 - steering_force) * direction_component.normalized_x + steering_force * movement_component.target_normalized_x
        new_dy = (1 - steering_force) * direction_component.normalized_y + steering_force * movement_component.target_normalized_y

        # Calculate the length (magnitude) of the direction vector for normalization
        # The operation **0.5 is equivalent to taking the square root of a number
        new_magnitude = (new_dx**2 + new_dy**2)**0.5
        if new_magnitude != 0:
            new_dx /= new_magnitude
            new_dy /= new_magnitude

        # Update the direction in the movement component
        direction_component.normalized_x = new_dx
        direction_component.normalized_y = new_dy


    def _apply_accelerate_and_decelerate(self, delta, movement_component: MovementComponent):
        if movement_component.distance_to_target is None:
            return

        # Determine current speed
        current_speed = movement_component.current_speed

        if movement_component.distance_to_target > movement_component.slow_down_distance:
            # Accelerate to max speed
            current_speed += movement_component.acceleration_rate * delta
        else:
            # Decelerate as we approach the target
            current_speed -= movement_component.deceleration_rate * delta

        # Clamp the speed between min and max values
        current_speed = max(movement_component.min_speed, min(current_speed, movement_component.speed))

        # Update the speed in the movement component
        movement_component.current_speed = current_speed


    def _calculate_velocity(self, delta, movement_component: MovementComponent, direction_component: DirectionComponent, velocity_component: VelocityComponent):
        if direction_component.normalized_x is None or direction_component.normalized_y is None:
            return

        # Calculate velocity based on direction and current speed
        velocity_component.x = direction_component.normalized_x * movement_component.current_speed * delta
        velocity_component.y = direction_component.normalized_y * movement_component.current_speed * delta


    def _apply_velocity(self, position_component: PositionComponent, velocity_component: VelocityComponent):
        position_component.x += velocity_component.x
        position_component.y += velocity_component.y


    def _update_move_target(self, movement_component: MovementComponent, position_component: PositionComponent, velocity_component: VelocityComponent):
        if movement_component.target_x is None or movement_component.target_y is None:
            velocity_component.x = 0
            velocity_component.y = 0
            print('target cancelled')
            return

        center_pos = position_component.get_center()
        distance = math.sqrt((movement_component.target_x - center_pos[0])**2 + (movement_component.target_y - center_pos[1])**2)
        if distance <= movement_component.target_reach_distance:
            movement_component.target_x = None
            movement_component.target_y = None
