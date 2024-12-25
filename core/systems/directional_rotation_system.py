import math
from core.components import DirectionComponent
from core.direction import Direction
from core.entities.protector import Protector


class DirectionalRotationSystem:
    def update(self, entities):
        for entity in entities:
            if hasattr(entity, 'movement_component') and hasattr(entity, 'directional_rotation_component') and hasattr(entity, 'direction_component'):
                direction_component: DirectionComponent = entity.direction_component
                self._calculate_direction_protector(entity, direction_component)


    def _calculate_direction_protector(self, entity, direction_component: DirectionComponent):
        if direction_component.normalized_x is None or direction_component.normalized_y is None:
            entity.directional_rotation_component.direction = Direction.EAST
            return

        # Gradually rotate towards target degrees
        target_degrees = self._direction_to_angle(direction_component.normalized_x, direction_component.normalized_y)
        current_degrees = entity.directional_rotation_component.degrees
        entity.directional_rotation_component.degrees = self._lerp_angle(
            current_degrees,
            target_degrees,
            entity.directional_rotation_component.rotation_speed)

        entity.directional_rotation_component.direction = self._get_direction(current_degrees)


    def _lerp_angle(self, current, target, step):
        """Linearly interpolate between two angles, handling wrapping."""
        difference = (target - current + 180) % 360 - 180  # Calculate shortest rotation path
        if abs(difference) <= step:  # If within step, snap to target
            return target
        return (current + step * (1 if difference > 0 else -1)) % 360


    def _get_direction(self, degrees):
        if  degrees > 337.5 or degrees <= 22.5:
            direction = Direction.NORTH
        elif 22.5 < degrees <= 67.5:
            direction = Direction.NORTH_EAST
        elif 67.5 < degrees <= 112.5:
            direction = Direction.EAST
        elif 112.5 < degrees <= 157.5:
            direction = Direction.SOUTH_EAST
        elif 157.5 < degrees <= 202.5:
            direction = Direction.SOUTH
        elif 202.5 < degrees <= 247.5:
            direction = Direction.SOUTH_WEST
        elif 247.5 < degrees <= 292.5:
            direction = Direction.WEST
        elif 292.5 < degrees <= 337.5:
            direction = Direction.NORTH_WEST
        else:
            direction = None  # Invalid angle
            print(f"invalid angle: {degrees}")

        return direction


    def _direction_to_angle(self, dx, dy):
        # Calculate the angle in radians
        radians = math.atan2(dy, dx)

        # Convert radians to degrees
        degrees = math.degrees(radians)

        # Ensure the angle is between 0 and 360 degrees
        if degrees < 0:
            degrees += 360

        return degrees