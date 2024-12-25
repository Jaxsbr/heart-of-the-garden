import pygame
from core.entities.heart import Heart
from core.entities.protector import Protector

SPRITE_COMPONENT = "sprite_component"
POSITION_COMPONENT = "position_component"
DIRECTIONAL_ROTATION_COMPONENT = "directional_rotation_component"

class RenderSystem:
    def __init__(self):
        pass

    def render(self, entities, screen):
        for entity in entities:
            requires_rotation = hasattr(entity, DIRECTIONAL_ROTATION_COMPONENT)

            if (hasattr(entity, SPRITE_COMPONENT) and
                hasattr(entity, POSITION_COMPONENT) and not
                requires_rotation):

                self._render(
                    screen,
                    entity.sprite_component.texture,
                    (entity.position_component.x, entity.position_component.y))

            elif (hasattr(entity, SPRITE_COMPONENT) and
                hasattr(entity, POSITION_COMPONENT) and
                requires_rotation):
                self._render_rotated(screen, entity)


    def _render_rotated(self, screen, entity):
        rotated_image = pygame.transform.rotate(
            entity.sprite_component.texture,
            -entity.directional_rotation_component.degrees)
        rotated_rect = rotated_image.get_rect(center=(entity.position_component.x, entity.position_component.y))
        self._render(screen, rotated_image, rotated_rect.topleft)


    def _render(self, screen, surface, pos):
        screen.blit(surface, pos)
