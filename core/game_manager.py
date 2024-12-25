from core.entity_factory import EntityFactory
from core.systems.directional_rotation_system import DirectionalRotationSystem
from core.systems.movement_system import MovementSystem
from core.systems.render_system import RenderSystem
import pygame

class GameManager:
    def __init__(self, screen, entity_factory: EntityFactory):
        self.screen = screen
        self.entity_factory = entity_factory
        self.clock = pygame.time.Clock()
        self._entities = []
        self._movement_system = MovementSystem()
        self._render_system = RenderSystem()
        self._directional_rotation_system = DirectionalRotationSystem()

        self._heart = self.entity_factory.create_heart()
        self._entities.append(self._heart)

        self._protector = self.entity_factory.create_protector()
        self._entities.append(self._protector)

    def handle_event(self, event):
        pass

    def update(self, delta):
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self._protector.movement_component.target_x = mouse_x
            self._protector.movement_component.target_y = mouse_y

        self._movement_system.update(self._entities, delta)
        self._directional_rotation_system.update(self._entities)

    def draw(self):
        self._render_system.render(self._entities, self.screen)

