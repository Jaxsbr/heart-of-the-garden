from dataclasses import dataclass
from config.game_settings import GameSettings
from core.components import AttackableComponent, DirectionalRotationComponent, EnemyAIComponent, MovementComponent, PositionComponent, SpriteComponent, VelocityComponent
from core.direction import Direction
from core.attack_priority import AttackPriority
from core.entities.enemy import Enemy
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
                y=self.game_settings.heart_start[1],
                w=self.game_settings.heart_size[0],
                h=self.game_settings.heart_size[1]),
            sprite_component=SpriteComponent(
                texture=self._get_texture("heart")),
            attackable_component=AttackableComponent(
                attack_priority=AttackPriority.HIGH))


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
                y=self.game_settings.protector_start[1],
                w=self.game_settings.protector_size[0],
                h=self.game_settings.protector_size[1]),
            sprite_component=SpriteComponent(
                texture=self._get_texture("protector")),
            directional_rotation_component=DirectionalRotationComponent(
                direction=Direction.EAST,
                rotation_speed=self.game_settings.protector_rotation_speed),
            attackable_component=AttackableComponent(
                attack_priority=AttackPriority.LOW))


    def create_enemy(self):
        # TODO: Using protector settings atm
        #       Replace with per enemy type config
        return Enemy(
            movement_component=MovementComponent(
                speed=self.game_settings.protector_speed,
                min_speed=self.game_settings.protector_min_speed,
                acceleration_rate=self.game_settings.protector_acceleration_rate,
                deceleration_rate=self.game_settings.protector_deceleration_rate,
                slow_down_distance=self.game_settings.protector_slowdown_distance,
                target_reach_distance=self.game_settings.protector_target_reach_distance,
                steering_force=self.game_settings.protector_steering_force),
            position_component=PositionComponent(
                x=300,
                y=50,
                w=self.game_settings.protector_size[0],
                h=self.game_settings.protector_size[1]),
            sprite_component=SpriteComponent(
                texture=self._get_texture("protector")),
            directional_rotation_component=DirectionalRotationComponent(
                direction=Direction.EAST,
                rotation_speed=self.game_settings.protector_rotation_speed),
            enemy_ai_component=EnemyAIComponent())


    def _get_texture(self, texture_name):
        asset_entry = self.asset_manifest.get_asset("textures", texture_name)
        return self.resource_manager.load(
            ResourceType.TEXTURE,
            texture_name,
            asset_entry["path"],
            (asset_entry["scale_x"], asset_entry["scale_y"]))
