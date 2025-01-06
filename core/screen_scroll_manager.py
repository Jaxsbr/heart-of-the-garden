from dataclasses import dataclass, field
import pygame

from core.resources.helpers import get_texture_resource
from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager


@dataclass
class ScreenScrollManager:
    screen_size: tuple[int, int]
    asset_manifest: AssetManifest
    resource_manager: ResourceManager
    gui_bar_rect: pygame.Rect
    horizontal_image: pygame.Surface = field(init=False)
    vertical_image: pygame.Surface = field(init=False)
    screen_offset_x: float = field(default=0)
    screen_offset_y: float = field(default=0)
    scroll_speed: float = field(default=2)
    edge_proximity_percent: float = field(default=0.05)
    screen_scroll_is_over: bool = field(default=False)
    screen_scroll_tick: float = field(default=0.2)
    screen_scroll_elapsed: float = field(default=0)
    near_left: bool = field(default=False)
    near_right: bool = field(default=False)
    near_top: bool = field(default=False)
    near_bottom: bool = field(default=False)

    def __post_init__(self):
        self.horizontal_image = get_texture_resource(
            self.asset_manifest, self.resource_manager, "scroll_horizontal"
        )
        self.vertical_image = get_texture_resource(
            self.asset_manifest, self.resource_manager, "scroll_vertical"
        )

        # TODO: replace 20 with percentage, edge_proximity_percent
        self.left_pos = (0, 0)
        self.right_pos = (self.screen_size[0] - 20, 0)
        self.top_pos = (0, 0)
        self.bottom_pos = (0, self.screen_size[1] - 20)

        self.horizontal_image = pygame.transform.scale(
            self.horizontal_image, (self.screen_size[0], 20)
        )

        self.vertical_image = pygame.transform.scale(
            self.vertical_image, (20, self.screen_size[1])
        )

    def update(self, delta):
        out_of_screen = self._is_out_of_screen()
        if out_of_screen:
            self.screen_scroll_elapsed = 0
            return

        self._update_screen_scroll(delta)

    def render(self, screen: pygame.Surface):
        if self.near_left:
            screen.blit(self.vertical_image, self.left_pos)
        if self.near_right:
            screen.blit(self.vertical_image, self.right_pos)
        if self.near_top:
            screen.blit(self.horizontal_image, self.top_pos)
        if self.near_bottom:
            screen.blit(self.horizontal_image, self.bottom_pos)

    def _is_out_of_screen(self) -> bool:
        mouseFocus = pygame.mouse.get_focused()
        if not mouseFocus:
            return True
        return False

    def _update_screen_scroll(self, delta):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Check mouse proximity to edges
        self.near_left = mouse_x < self.screen_size[0] * self.edge_proximity_percent
        self.near_right = mouse_x > self.screen_size[0] * (
            1 - self.edge_proximity_percent
        )
        self.near_top = mouse_y < self.screen_size[1] * self.edge_proximity_percent
        self.near_bottom = mouse_y > self.screen_size[1] * (
            1 - self.edge_proximity_percent
        )

        # Update scroll timer
        if self.near_left or self.near_right or self.near_top or self.near_bottom:
            self.screen_scroll_elapsed += delta
        else:
            self.screen_scroll_elapsed = 0

        # Apply screen offset (movement)
        if self.screen_scroll_elapsed >= self.screen_scroll_tick:
            if self.near_left:
                self.screen_offset_x += self.scroll_speed
            if self.near_right:
                self.screen_offset_x -= self.scroll_speed
            if self.near_top:
                self.screen_offset_y += self.scroll_speed
            if self.near_bottom:
                self.screen_offset_y -= self.scroll_speed
