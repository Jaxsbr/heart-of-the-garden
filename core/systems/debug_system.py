from dataclasses import dataclass, field
import pygame
from core.components.attackable_component import AttackableComponent
from core.components.controllable_component import ControllableComponent
from core.components.interaction_component import InteractionComponent
from core.components.movement_component import MovementComponent
from core.entities.entity import Entity

@dataclass
class DebugSystem:
    _debug_font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self._debug_font = pygame.font.Font(pygame.font.get_default_font(), 20)

    def render_debug(self, screen, entities: list[Entity]):
        x = 900
        y = 50
        texts = []
        for entity in entities:
            attackable = entity.get_component(AttackableComponent)
            controllable = entity.get_component(ControllableComponent)
            interaction = entity.get_component(InteractionComponent)
            movement = entity.get_component(MovementComponent)

            # heart
            if (
                attackable is not None
                and interaction is not None
                and controllable is None
            ):
                texts.append("--HEART--")
                texts.append(
                    f"interaction duration: {interaction.interaction_duration}"
                )

            # protector
            if (
                attackable is not None
                and interaction is not None
                and controllable is not None
                and movement is not None
            ):
                texts.append("--PROTECTOR--")
                texts.append(
                    f"interaction duration: {interaction.interaction_duration}"
                )
                texts.append(
                    f"move target: x:{movement.target_x} y:{movement.target_y}"
                )
                texts.append(f"distance to target: {movement.distance_to_target}")
                texts.append(f"target reach distance: {movement.target_reach_distance}")

        for index in range(len(texts)):
            text_surface = self._debug_font.render(texts[index], True, "black")
            text_rect = text_surface.get_rect(topleft=(x, y))
            screen.blit(text_surface, text_rect)
            y += 25
