import pygame

from core.components.directional_rotation_component import DirectionalRotationComponent
from core.components.position_component import PositionComponent
from core.components.sprite_component import SpriteComponent
from core.entities.entity import Entity


class RenderSystem:
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

                # TODO: extract "10" from proper settings
                # if entity.selection_component.is_selected:
                color = "green"
                center_pos = position_component.get_center()
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        center_pos[0] - position_component.w / 4,
                        position_component.y - 10,
                        position_component.w / 2,
                        10,
                    ),
                )
            else:
                self._render(
                    screen,
                    entity.sprite_component.texture,
                    (position_component.x, position_component.y),
                )

                # TODO: extract "10" from proper settings
                # if entity.selection_component.is_selected:
                color = "green"
                center_pos = position_component.get_center()
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(
                        center_pos[0] - position_component.w / 4,
                        position_component.y - 10,
                        position_component.w / 2,
                        10,
                    ),
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
        self._render(screen, rotated_image, rotated_rect.topleft)

    def _render(self, screen, surface, pos):
        # pygame.draw.rect(screen, "blue", entity.position_component.get_bounds())

        # pygame.draw.circle(screen, "red", (entity.position_component.x, entity.position_component.y), 5)

        # center_pos = entity.position_component.get_center()
        # pygame.draw.circle(screen, "pink", center_pos, 5)

        # if hasattr(entity, Component.MOVEMENT):
        #     if entity.movement_component.target_x is not None and entity.movement_component.target_y is not None:
        #         pygame.draw.circle(screen, "orange", (entity.movement_component.target_x, entity.movement_component.target_y), 20)

        screen.blit(surface, pos)
