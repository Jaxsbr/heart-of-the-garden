from dataclasses import dataclass
from config.game_settings import GameSettings
from core.components import DirectionalRotationComponent, MovementComponent, PositionComponent, SpriteComponent, VelocityComponent
from core.direction import Direction
from core.entities.heart import Heart
from core.entities.protector import Protector
from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager
from core.resources.resource_type import ResourceType

@dataclass
class EntityFactory:
    asset_manifest: AssetManifest
    resource_manager: ResourceManager
    game_settings: GameSettings

    def create_heart(self):
        return Heart(
            position_component=PositionComponent(
                x=self.game_settings.heart_start[0],
                y=self.game_settings.heart_start[1]),
            sprite_component=SpriteComponent(
                texture=self._get_texture("heart")))


    def create_protector(self):
        return Protector(
            movement_component=MovementComponent(
                speed=self.game_settings.protector_speed,
                min_speed=self.game_settings.protector_min_speed,
                acceleration_rate=self.game_settings.protector_acceleration_rate,
                deceleration_rate=self.game_settings.protector_deceleration_rate,
                slow_down_distance=self.game_settings.protector_slowdown_distance,
                target_reach_distance=self.game_settings.protector_target_reach_distance,
                steering_force=self.game_settings.protector_steering_force),
            position_component=PositionComponent(
                x=self.game_settings.protector_start[0],
                y=self.game_settings.protector_start[1]),
            sprite_component=SpriteComponent(
                texture=self._get_texture("protector")),
            directional_rotation_component=DirectionalRotationComponent(
                direction=Direction.EAST,
                rotation_speed=self.game_settings.protector_rotation_speed
            ))


    def _get_texture(self, texture_name):
        asset_entry = self.asset_manifest.get_asset("textures", texture_name)

        return self.resource_manager.load(
            ResourceType.TEXTURE,
            texture_name,
            asset_entry["path"],
            (asset_entry["scale_x"], asset_entry["scale_y"]))
