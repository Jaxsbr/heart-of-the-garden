from core.entities.enemy import Enemy
from core.entity_factory import EntityFactory
from core.eventing.event_dispatcher import EventDispatcher
from core.systems.directional_rotation_system import DirectionalRotationSystem
from core.systems.encounter_system import EncounterSystem
from core.systems.enemy_ai_system import EnemyAISystem
from core.systems.enemy_spawn_system import EnemySpawnSystem
from core.systems.entity_control_system import EntityControlSystem
from core.systems.movement_system import MovementSystem
from core.systems.render_system import RenderSystem
import pygame

from core.systems.selection_system import SelectionSystem

class GameManager:
    def __init__(self, screen, entity_factory: EntityFactory):
        self.screen = screen
        self.entity_factory = entity_factory
        self.clock = pygame.time.Clock()
        self.event_dispatcher = EventDispatcher()
        self._entities = []
        self._movement_system = MovementSystem()
        self._render_system = RenderSystem()
        self._directional_rotation_system = DirectionalRotationSystem()

        self._heart = self.entity_factory.create_heart()
        self._entities.append(self._heart)

        self._protector = self.entity_factory.create_protector()
        self._entities.append(self._protector)

        self._enemy_spawn_system = EnemySpawnSystem()
        self._enemy_ai_system = EnemyAISystem(self.event_dispatcher)
        self._selection_system = SelectionSystem(self.event_dispatcher)
        self._entity_control_system = EntityControlSystem(self.event_dispatcher)
        self._encounter_system = EncounterSystem(self.event_dispatcher)


    def _create_enemy(self) -> Enemy:
        enemy = self.entity_factory.create_enemy()
        self._entities.append(enemy)
        return enemy


    def handle_event(self, event):
        pass


    def update(self, delta):
        self._movement_system.update(self._entities, delta)
        self._directional_rotation_system.update(self._entities)
        self._enemy_spawn_system.update(delta, self._create_enemy)
        self._enemy_ai_system.update(self._entities, delta)
        self._selection_system.update(delta, self._entities)
        self._entity_control_system.update(delta, self._entities)
        self._encounter_system.update(delta, self._entities)


    def draw(self):
        self._render_system.render(self._entities, self.screen)

