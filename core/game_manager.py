from core.entities.entity import Entity
from core.entity_factory import EntityFactory
from core.eventing.base_event import BaseEvent
from core.eventing.event_dispatcher import EventDispatcher
from core.eventing.event_types import EventTypes
from core.screen_position_helper import get_random_not_overlapping_in_bounds_pos
from core.screen_scroll_manager import ScreenScrollManager
from core.systems.collision_system import CollisionSystem
from core.systems.debug_system import DebugSystem
from core.systems.directional_rotation_system import DirectionalRotationSystem
from core.systems.enemy_ai_system import EnemyAISystem
from core.systems.gui_selection_system import GUISelectionSystem
from core.systems.interaction_system import InteractionSystem
from core.systems.enemy_spawn_system import EnemySpawnSystem
from core.systems.entity_control_system import EntityControlSystem
from core.systems.movement_system import MovementSystem
from core.systems.render_system import RenderSystem
import pygame

from core.systems.retreat_movement_system import RetreatMovementSystem
from core.systems.retreat_system import RetreatSystem
from core.systems.selection_system import SelectionSystem
from core.ui.hud import HUD


class GameManager:
    def __init__(
        self,
        screen,
        screen_size,
        event_dispatcher: EventDispatcher,
        entity_factory: EntityFactory,
        screen_scroll_manager: ScreenScrollManager,
        hud: HUD,
    ):
        self.event_dispatcher = event_dispatcher
        self.screen = screen
        self.screen_size = screen_size
        self.entity_factory = entity_factory
        self.clock = pygame.time.Clock()
        self.screen_scroll_manager = screen_scroll_manager
        self._hud = hud

        self._gui_selection_system = GUISelectionSystem(self.event_dispatcher)
        self._movement_system = MovementSystem()
        self._render_system = RenderSystem()
        self._directional_rotation_system = DirectionalRotationSystem()
        self._enemy_spawn_system = EnemySpawnSystem(self.screen_size)
        self._enemy_ai_system = EnemyAISystem(self.event_dispatcher)
        self._selection_system = SelectionSystem(self.event_dispatcher)
        self._entity_control_system = EntityControlSystem(
            self.event_dispatcher, move_exclusion_zones=[self._hud.gui_buttons_rect]
        )
        self._interaction_system = InteractionSystem(self.event_dispatcher)
        self._retreat_system = RetreatSystem(self.screen_size)
        self._retreat_movement_system = RetreatMovementSystem()
        self._collision_system = CollisionSystem()
        self._debug_system = DebugSystem()

        self._heart = self.entity_factory.create_heart()
        self._protector = self.entity_factory.create_protector()

        self._entities = []
        self._entities.append(self._heart)
        self._entities.append(self._protector)

        for p in range(10):
            pos = None
            while pos is None:
                pos = get_random_not_overlapping_in_bounds_pos(
                    self.screen_size, (64, 64), self._entities
                )
            plant = self.entity_factory.create_plant(pos.x, pos.y)
            self._entities.append(plant)
        print("found spots for all plants")

    def _create_enemy(self, start_pos: pygame.Vector2) -> Entity:
        enemy = self.entity_factory.create_enemy(start_pos)
        self._entities.append(enemy)
        return enemy

    def handle_event(self, event):
        pass

    def update(self, delta):
        screen_offset = (
            self.screen_scroll_manager.screen_offset_x,
            self.screen_scroll_manager.screen_offset_y,
        )

        self._gui_selection_system.update(self._entities)
        self._movement_system.update(self._entities, delta)
        self._directional_rotation_system.update(self._entities)
        self._enemy_spawn_system.update(delta, self._create_enemy)
        self._enemy_ai_system.update(self._entities, delta)
        self._selection_system.update(delta, self._entities)
        self._entity_control_system.update(delta, self._entities, screen_offset)
        self._interaction_system.update()
        self._retreat_system.update(self._entities)
        self._retreat_movement_system.update(delta, self._entities)
        self._collision_system.update(delta, self._entities)
        self.screen_scroll_manager.update(delta)
        self._render_system.update(screen_offset)
        self._hud.update()

    def draw(self):
        # TEMP: Simulate a map with this rect
        pygame.draw.rect(
            self.screen,
            "skyblue",
            pygame.Rect(
                self.screen_scroll_manager.screen_offset_x,
                self.screen_scroll_manager.screen_offset_y,
                self.screen_size[0],
                self.screen_size[1],
            ),
        )

        self._render_system.render(self._entities, self.screen)
        self._hud.render(self.screen)
        self._gui_selection_system.render(self.screen)
        self.screen_scroll_manager.render(self.screen)
        self._debug_system.render_debug(self.screen, self._entities)
