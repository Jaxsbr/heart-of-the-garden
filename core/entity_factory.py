from dataclasses import dataclass

import pygame
from config.game_settings import GameSettings
from core.components.attackable_component import AttackableComponent
from core.components.controllable_component import ControllableComponent
from core.components.direction_component import DirectionComponent
from core.components.directional_rotation_component import DirectionalRotationComponent
from core.components.encounter_component import EncounterComponent
from core.components.enemy_ai_component import EnemyAIComponent
from core.components.movement_component import MovementComponent
from core.components.position_component import PositionComponent
from core.components.selection_component import SelectionComponent
from core.components.sprite_component import SpriteComponent
from core.components.velocity_component import VelocityComponent
from core.direction import Direction
from core.attack_priority import AttackPriority
from core.entities.entity import Entity
from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager
from core.resources.resource_type import ResourceType


@dataclass
class EntityFactory:
    asset_manifest: AssetManifest
    resource_manager: ResourceManager
    game_settings: GameSettings

    def _create_living_entity(
        self, bounds: pygame.Rect, sprite_component: SpriteComponent
    ) -> Entity:
        base_entity = Entity(
            position_component=PositionComponent(
                x=bounds.x,
                y=bounds.y,
                w=bounds.w,
                h=bounds.h,
            ),
            sprite_component=sprite_component,
            velocity_component=VelocityComponent(),
            direction_component=DirectionComponent(),
        )
        base_entity.add_component(SelectionComponent())
        base_entity.add_component(EncounterComponent())
        return base_entity

    def create_heart(self):
        left = self.game_settings.heart_start[0]
        top = self.game_settings.heart_start[1]
        width = self.game_settings.heart_size[0]
        height = self.game_settings.heart_size[1]
        heart = self._create_living_entity(
            pygame.Rect(left, top, width, height),
            SpriteComponent(texture=self._get_texture("heart")),
        )
        heart.add_component(AttackableComponent(attack_priority=AttackPriority.HIGH))
        return heart

    def create_protector(self):
        left = self.game_settings.protector_start[0]
        top = self.game_settings.protector_start[1]
        width = self.game_settings.protector_size[0]
        height = self.game_settings.protector_size[1]
        protector = self._create_living_entity(
            pygame.Rect(left, top, width, height),
            SpriteComponent(texture=self._get_texture("protector")),
        )
        protector.add_component(
            MovementComponent(
                speed=self.game_settings.protector_speed,
                min_speed=self.game_settings.protector_min_speed,
                acceleration_rate=self.game_settings.protector_acceleration_rate,
                deceleration_rate=self.game_settings.protector_deceleration_rate,
                slow_down_distance=self.game_settings.protector_slowdown_distance,
                target_reach_distance=self.game_settings.protector_target_reach_distance,
                steering_force=self.game_settings.protector_steering_force,
            )
        )
        protector.add_component(
            DirectionalRotationComponent(
                direction=Direction.EAST,
                rotation_speed=self.game_settings.protector_rotation_speed,
            )
        )
        protector.add_component(AttackableComponent(attack_priority=AttackPriority.LOW))
        protector.add_component(ControllableComponent())
        return protector

    def create_plant(self):
        # TODO: plant entity, must be attackable
        pass

    def create_enemy(self):
        # TODO: Using protector settings atm
        #       Replace with per enemy type config\
        left = 300
        top = 50
        width = self.game_settings.protector_size[0]
        height = self.game_settings.protector_size[1]
        enemy = self._create_living_entity(
            pygame.Rect(left, top, width, height),
            SpriteComponent(texture=self._get_texture("spider")),
        )
        enemy.add_component(
            MovementComponent(
                speed=self.game_settings.protector_speed,
                min_speed=self.game_settings.protector_min_speed,
                acceleration_rate=self.game_settings.protector_acceleration_rate,
                deceleration_rate=self.game_settings.protector_deceleration_rate,
                slow_down_distance=self.game_settings.protector_slowdown_distance,
                target_reach_distance=self.game_settings.protector_target_reach_distance,
                steering_force=self.game_settings.protector_steering_force,
            )
        )
        enemy.add_component(
            DirectionalRotationComponent(
                direction=Direction.EAST,
                rotation_speed=self.game_settings.protector_rotation_speed,
            )
        )
        enemy.add_component(EnemyAIComponent())
        return enemy

    def _get_texture(self, texture_name):
        asset_entry = self.asset_manifest.get_asset("textures", texture_name)
        return self.resource_manager.load(
            ResourceType.TEXTURE,
            texture_name,
            asset_entry["path"],
            (asset_entry["scale_x"], asset_entry["scale_y"]),
        )
