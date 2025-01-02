from dataclasses import dataclass, field
from typing import Callable

import pygame

from core.entities.entity import Entity
from core.screen_position_helper import get_random_start_pos


@dataclass
class EnemySpawnSystem:
    screen_size: tuple[int, int]
    spawn_elapsed: float = field(default=9)
    spawn_tick: float = field(default=2)

    def update(self, delta, create_enemy_function: Callable[[pygame.Vector2], Entity]):
        self._set_spawn_config()

        self.spawn_elapsed += delta * 1
        if self.spawn_elapsed >= self.spawn_tick:
            self.spawn_elapsed = 0
            start_pos = get_random_start_pos(self.screen_size)
            enemy = create_enemy_function(start_pos)

    def _set_spawn_config(self):
        # TODO: config changes as wave progress
        self.spawn_tick = 2  # TODO: get from config
