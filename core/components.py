from dataclasses import dataclass, field
from enum import Enum
from core.direction import Direction
import pygame


class Component():
    POSITION = "position_component"
    VELOCITY = "velocity_component"
    MOVEMENT = "movement_component"
    DIRECTION = "direction_component"
    DIRECTIONAL_ROTATION = "directional_rotation_component"
    SPRITE = "sprite_component"


@dataclass
class PositionComponent:
    x: float
    y: float


@dataclass
class VelocityComponent:
    x: float = field(default=0)
    y: float = field(default=0)


@dataclass
class MovementComponent:
    speed: float
    min_speed: float
    acceleration_rate: float
    deceleration_rate: float
    slow_down_distance: float
    target_reach_distance: float
    steering_force: float
    current_speed: float = field(default=0)
    target_x: float | None = field(default=None)
    target_y: float | None = field(default=None)
    target_normalized_x: float | None = field(default=None)
    target_normalized_y: float | None = field(default=None)
    distance_to_target: float | None = field(default=None)


@dataclass
class DirectionComponent:
    normalized_x: float | None = field(default=None)
    normalized_y: float | None = field(default=None)


@dataclass
class DirectionalRotationComponent:
    direction: Direction
    degrees: float = field(default=0)
    rotation_speed: float = field(default=5)


@dataclass
class SpriteComponent:
    texture: pygame.Surface
