from dataclasses import dataclass

import pygame

from core.components.living_entity_component import LivingEntityComponent


@dataclass
class PositionComponent(LivingEntityComponent):
    x: float
    y: float
    w: float
    h: float

    def get_center(self):
        return (self.x + self.w / 2, self.y + self.h / 2)

    def get_bounds(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def get_inner_radius(self) -> float:
        return min(self.w, self.h) // 2

    def get_outer_radius(self) -> float:
        # center to any corner
        return self.distance_to_center((self.x, self.y))

    def distance_to_center(self, point) -> float:
        center_pos = self.get_center()
        x = point[0] - center_pos[0]
        y = point[1] - center_pos[1]
        return (x**2 + y**2) ** 0.5

    def intersects(self, rect: pygame.Rect) -> bool:
        bounds = self.get_bounds()
        return bounds.colliderect(rect)

    def within_center_distance(self, distance, point):
        distance_to_target = self.distance_to_center(point)
        return distance >= distance_to_target

    def contains_point(self, point) -> bool:
        return self.get_bounds().collidepoint(point[0], point[1])
