from dataclasses import dataclass
import pygame

from core.components.living_entity_component import LivingEntityComponent

@dataclass
class SpriteComponent(LivingEntityComponent):
    texture: pygame.Surface
