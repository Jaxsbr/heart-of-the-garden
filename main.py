from config.game_settings import GameSettings
from core.entity_factory import EntityFactory
from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager
from core.resources.resource_type import ResourceType
import pygame
from core.game_manager import GameManager

def main():
    pygame.init()
    screen_width = 800
    clock = pygame.time.Clock()
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Heart of the Garden")

    asset_manifest = AssetManifest("assets/asset_manifest.json")
    resource_manager = ResourceManager()
    game_settings = GameSettings()
    entity_factory = EntityFactory(asset_manifest, resource_manager, game_settings)

    game_manager = GameManager(screen, entity_factory)

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
