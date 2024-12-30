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

    def intersects(self, rect: pygame.Rect) -> bool:
        bounds = self.get_bounds()
        return bounds.colliderect(rect)

    def within_center_distance(self, distance, point):
        center_pos = self.get_center()
        x = point[0] - center_pos[0]
        y = point[1] - center_pos[1]
        distance_to_target = (x**2 + y**2) ** 0.5
        return distance >= distance_to_target

    def contains_point(self, point) -> bool:
        return self.get_bounds().collidepoint(point[0], point[1])
