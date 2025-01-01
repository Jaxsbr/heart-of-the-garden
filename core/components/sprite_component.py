from dataclasses import dataclass
import pygame

from core.components.component import Component
from core.components.living_entity_component import LivingEntityComponent


@dataclass
class SpriteComponent(LivingEntityComponent):
    texture: pygame.Surface
    width: int
    height: int
