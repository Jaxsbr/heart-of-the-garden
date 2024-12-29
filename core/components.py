from dataclasses import dataclass, field
from core.direction import Direction
import pygame


class Component():
    POSITION = "position_component"
    VELOCITY = "velocity_component"
    MOVEMENT = "movement_component"
    DIRECTION = "direction_component"
    DIRECTIONAL_ROTATION = "directional_rotation_component"
    SPRITE = "sprite_component"
    HEALTH = "health_component"
    ENEMY_AI = "enemy_ai_component"
    ATTACKABLE = "attackable_component"
    SELECTION = "selection_component"
    CONTROLLABLE = "controllable_component"
    ENCOUNTER = "encounter_component"


@dataclass
class PositionComponent(pygame.sprite.Sprite):
    x: float
    y: float
    w: float
    h: float

    def get_center(self):
        return (
            self.x + self.w / 2,
            self.y + self.h / 2)


    def get_bounds(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)


    def intersects(self, rect: pygame.Rect) -> bool:
        bounds = self.get_bounds()
        return bounds.colliderect(rect)


    def within_center_distance(self, distance, point):
        center_pos = self.get_center()
        x = point[0] - center_pos[0]
        y = point[1] - center_pos[1]
        distance_to_target = (x**2 + y**2)**0.5
        return distance >= distance_to_target


    def contains_point(self, point) -> bool:
        return self.get_bounds().collidepoint(point[0], point[1])


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


@dataclass
class HealthComponent:
    hp: int
    max_hp: int
    remaining_hp_percentage: float = field(default=100)
    alive: bool = field(default=False)


@dataclass
class EnemyAIComponent:
    has_attack_target: bool | None = field(default=False)


@dataclass
class AttackableComponent:
    attack_priority: int


@dataclass
class SelectionComponent:
    is_selected: bool = field(default=False)


class ControllableComponent:
    pass


@dataclass
class EncounterComponent:
    encounter_points: int = field(default=0)
    max_encounter_points_reached: bool = field(default=False)
    is_fleeing: bool = field(default=False)
    flee_tick: float = field(default=10)
    flee_elapsed: float = field(default=0)


@dataclass
class FleeComponent:
    is_fleeing: bool = field(default=False)
    flee_tick: float = field(default=10)
    flee_elapsed: float = field(default=0)
