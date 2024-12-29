import pygame
from core.components import Component, PositionComponent

class RenderSystem:
    def render(self, entities, screen):
        for entity in entities:
            if not self._has_valid_components(entity):
                continue

            position_component: PositionComponent = entity.position_component

            requires_rotation = self._has_directional_rotation(entity)
            if requires_rotation:
                self._render_rotated(screen, entity)

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
                        10))
            else:
                self._render(
                    screen,
                    entity.sprite_component.texture,
                    (position_component.x, position_component.y),
                    entity)

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
                        10))


    def _has_valid_components(self, entity) -> bool:
        return (
            hasattr(entity, Component.SPRITE) and
            hasattr(entity, Component.POSITION) and
            hasattr(entity, Component.SELECTION))


    def _has_directional_rotation(self, entity) -> bool:
        return hasattr(entity, Component.DIRECTIONAL_ROTATION)


    def _render_rotated(self, screen, entity):
        rotated_image = pygame.transform.rotate(
            entity.sprite_component.texture,
            -entity.directional_rotation_component.degrees)
        center_pos = entity.position_component.get_center()
        rotated_rect = rotated_image.get_rect(center=(center_pos[0], center_pos[1]))
        self._render(screen, rotated_image, rotated_rect.topleft, entity)


    def _render(self, screen, surface, pos, entity):
        # pygame.draw.rect(screen, "blue", entity.position_component.get_bounds())

        # pygame.draw.circle(screen, "red", (entity.position_component.x, entity.position_component.y), 5)

        # center_pos = entity.position_component.get_center()
        # pygame.draw.circle(screen, "pink", center_pos, 5)

        # if hasattr(entity, Component.MOVEMENT):
        #     if entity.movement_component.target_x is not None and entity.movement_component.target_y is not None:
        #         pygame.draw.circle(screen, "orange", (entity.movement_component.target_x, entity.movement_component.target_y), 20)

        screen.blit(surface, pos)
