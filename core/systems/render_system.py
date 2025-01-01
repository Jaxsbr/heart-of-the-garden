from dataclasses import dataclass, field
import pygame

from core.components.directional_rotation_component import DirectionalRotationComponent
from core.components.position_component import PositionComponent
from core.components.sprite_component import SpriteComponent
from core.entities.entity import Entity


@dataclass
class RenderSystem:
    screen_offset_x: float = field(default=0)
    screen_offset_y: float = field(default=0)

    def update(self, screen_offset):
        self.screen_offset_x = screen_offset[0]
        self.screen_offset_y = screen_offset[1]

    def render(self, entities: list[Entity], screen):
        for entity in entities:
            position_component: PositionComponent = entity.position_component

            directional_rotation_component = entity.get_component(
                DirectionalRotationComponent
            )
            if directional_rotation_component is not None:
                sprite_component = entity.sprite_component
                self._render_rotated(
                    screen,
                    sprite_component,
                    position_component,
                    directional_rotation_component,
                )
            else:
                self._render(
                    screen,
                    entity.sprite_component.texture,
                    (position_component.x, position_component.y),
                    (entity.sprite_component.width, entity.sprite_component.height),
                )

    def _render_rotated(
        self,
        screen,
        sprite_component: SpriteComponent,
        position_component: PositionComponent,
        directional_rotation_component: DirectionalRotationComponent,
    ):
        rotated_image = pygame.transform.rotate(
            sprite_component.texture,
            -directional_rotation_component.degrees,
        )
        center_pos = position_component.get_center()
        rotated_rect = rotated_image.get_rect(center=(center_pos[0], center_pos[1]))
        self._render(
            screen,
            rotated_image,
            rotated_rect.topleft,
            (sprite_component.width, sprite_component.height),
        )

    def _render(self, screen, surface, pos, size):
        screen_pos = (pos[0] + self.screen_offset_x, pos[1] + self.screen_offset_y)
        screen.blit(surface, screen_pos)
