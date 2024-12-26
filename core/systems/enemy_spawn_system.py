from dataclasses import dataclass, field
from typing import Callable
from core.entities.enemy import Enemy

@dataclass
class EnemySpawnSystem:
    """
    This class is responsible for:
    - Orchestrating enemy waves for the current stage
    - Spawning enemies
    - Orchestrate wave phases
    - Raise wave events (win lose)
    """
    spawn_elapsed: float = field(default=0)
    spawn_tick: float = field(default=0)

    def update(self, delta, create_enemy_function: Callable[[], Enemy]):
        self._set_spawn_config()

        self.spawn_elapsed += delta * 1
        if self.spawn_elapsed >= self.spawn_tick:
            self.spawn_elapsed = 0
            enemy = create_enemy_function()


    def _set_spawn_config(self):
        # TODO: config changes as wave progress
        self.spawn_tick = 20 # TODO: get from config

