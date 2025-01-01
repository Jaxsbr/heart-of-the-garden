from dataclasses import dataclass
import random

import pygame
from config.game_settings import GameSettings
from core.components.attackable_component import AttackableComponent
from core.components.controllable_component import ControllableComponent
from core.components.direction_component import DirectionComponent
from core.components.directional_rotation_component import DirectionalRotationComponent
from core.components.interaction_component import InteractionComponent
from core.components.enemy_ai_component import EnemyAIComponent
from core.components.retreat_component import RetreatComponent
from core.components.movement_component import MovementComponent
from core.components.position_component import PositionComponent
from core.components.retreate_behavior_component import RetreatBehaviorComponent
from core.components.selection_component import SelectionComponent
from core.components.sprite_component import SpriteComponent
from core.components.velocity_component import VelocityComponent
from core.direction import Direction
from core.attack_priority import AttackPriority
from core.entities.entity import Entity
from core.resources.helpers import get_texture_resource
from core.resources.manifest import AssetManifest
from core.resources.resource_manager import ResourceManager
from core.retreat_move_types import RetreatMoveTypes


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
        base_entity.add_component(InteractionComponent())
        return base_entity

    def create_heart(self):
        left = self.game_settings.heart_start[0]
        top = self.game_settings.heart_start[1]
        width = self.game_settings.heart_size[0]
        height = self.game_settings.heart_size[1]
        heart = self._create_living_entity(
            pygame.Rect(left, top, width, height),
            SpriteComponent(
                texture=get_texture_resource(
                    self.asset_manifest, self.resource_manager, "heart"
                ),
                width=self.game_settings.heart_size[0],
                height=self.game_settings.heart_size[1],
            ),
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
            SpriteComponent(
                texture=get_texture_resource(
                    self.asset_manifest, self.resource_manager, "protector"
                ),
                width=self.game_settings.protector_size[0],
                height=self.game_settings.protector_size[1],
            ),
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
        protector.add_component(RetreatComponent())
        protector.add_component(
            RetreatBehaviorComponent(move_type=RetreatMoveTypes.BOLT)
        )
        return protector

    def create_plant(self):
        # TODO: plant entity, must be attackable
        pass

    def create_enemy(self, start_pos: pygame.Vector2):
        # TODO: Using protector settings atm
        #       Replace with per enemy type config\
        width = self.game_settings.protector_size[0]
        height = self.game_settings.protector_size[1]
        enemy = self._create_living_entity(
            pygame.Rect(start_pos.x, start_pos.y, width, height),
            SpriteComponent(
                texture=get_texture_resource(
                    self.asset_manifest, self.resource_manager, "spider"
                ),
                width=self.game_settings.protector_size[0],
                height=self.game_settings.protector_size[1],
            ),
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
        enemy.add_component(RetreatComponent())
        enemy.add_component(
            RetreatBehaviorComponent(
                move_type=RetreatMoveTypes.WIGGLE,
                retreat_direction=self.get_random_direction(),
            )
        )
        enemy.add_component(EnemyAIComponent())
        return enemy

    def get_random_direction(self):
        while True:
            x = random.choice([-1, 0, 1])
            y = random.choice([-1, 0, 1])
            if x != 0 or y != 0:  # Ensure movement
                return (x, y)
