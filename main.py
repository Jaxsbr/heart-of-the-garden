from config.game_settings import GameSettings
from core.entity_factory import EntityFactory
from core.eventing.event_dispatcher import EventDispatcher
from core.resources.helpers import get_texture_resource
from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager
import pygame
from core.game_manager import GameManager
from core.screen_scroll_manager import ScreenScrollManager
from core.ui.hud import HUD


def main():
    pygame.init()
    clock = pygame.time.Clock()
    game_settings = GameSettings()
    screen_size = game_settings.world_bounds
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Heart of the Garden")

    asset_manifest = AssetManifest("assets/asset_manifest.json")
    resource_manager = ResourceManager()
    entity_factory = EntityFactory(asset_manifest, resource_manager, game_settings)
    event_dispatcher = EventDispatcher()

    hud = HUD(
        event_dispatcher,
        screen_size,
        get_texture_resource(asset_manifest, resource_manager, "gui_bar"),
        get_texture_resource(asset_manifest, resource_manager, "gui_buttons"),
    )
    screen_scroll_manager = ScreenScrollManager(
        screen_size, asset_manifest, resource_manager, hud.gui_bar_rect
    )
    game_manager = GameManager(
        screen,
        screen_size,
        event_dispatcher,
        entity_factory,
        screen_scroll_manager,
        hud,
    )

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)

        delta = clock.tick(60) / 1000
        game_manager.update(delta)
        screen.fill("cornflowerblue")
        game_manager.draw()

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
