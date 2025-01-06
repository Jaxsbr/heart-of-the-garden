from dataclasses import dataclass
import random

import pygame
from config.game_settings import GameSettings
from core.components.attackable_component import AttackableComponent
from core.components.collision_component import CollisionComponent
from core.components.controllable_component import ControllableComponent
from core.components.direction_component import DirectionComponent
from core.components.directional_rotation_component import DirectionalRotationComponent
from core.components.gui_selection_component import GUISelectionComponent
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
from core.ui.gui_types import GUITypes


@dataclass
class EntityFactory:
    asset_manifest: AssetManifest
    resource_manager: ResourceManager
    game_settings: GameSettings

    def _create_base_entity(
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
        return base_entity

    def _create_gui_entity(
        self, bounds: pygame.Rect, sprite_component: SpriteComponent, gui_type: GUITypes
    ) -> Entity:
        base_entity = self._create_base_entity(bounds, sprite_component)
        base_entity.add_component(GUISelectionComponent(gui_type=gui_type))
        return base_entity

    def _create_living_entity(
        self, bounds: pygame.Rect, sprite_component: SpriteComponent
    ) -> Entity:
        base_entity = base_entity = self._create_base_entity(bounds, sprite_component)
        # base_entity.add_component(SelectionComponent())
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
        heart.add_component(CollisionComponent(weight=self.game_settings.heart_weight))
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
        protector.add_component(
            CollisionComponent(weight=self.game_settings.protector_weight)
        )
        return protector

    def create_plant(self, x, y):
        # TODO: Use plant settings from config
        left = x
        top = y
        width = self.game_settings.heart_size[0] // 2
        height = self.game_settings.heart_size[1] // 2
        plant = self._create_living_entity(
            pygame.Rect(left, top, width, height),
            SpriteComponent(
                texture=get_texture_resource(
                    self.asset_manifest, self.resource_manager, "plant1"
                ),
                width=width,
                height=height,
            ),
        )
        plant.add_component(AttackableComponent(attack_priority=AttackPriority.MEDIUM))
        plant.add_component(CollisionComponent(weight=self.game_settings.heart_weight))
        return plant

    def create_enemy(self, start_pos: pygame.Vector2):
        enemy_packet = self.get_variable_enemy_packet()
        width = enemy_packet[2]
        height = enemy_packet[3]
        enemy = self._create_living_entity(
            pygame.Rect(start_pos.x, start_pos.y, width, height),
            SpriteComponent(
                texture=get_texture_resource(
                    self.asset_manifest,
                    self.resource_manager,
                    "spider",
                    width,
                    height,
                    enemy_packet[0],
                ),
                width=width,
                height=height,
            ),
        )
        enemy.add_component(
            MovementComponent(
                speed=enemy_packet[4],
                min_speed=self.game_settings.enemy_speed,
                acceleration_rate=self.game_settings.enemy_acceleration_rate,
                deceleration_rate=self.game_settings.enemy_deceleration_rate,
                slow_down_distance=self.game_settings.enemy_slowdown_distance,
                target_reach_distance=self.game_settings.enemy_target_reach_distance,
                steering_force=self.game_settings.enemy_steering_force,
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
        enemy.add_component(CollisionComponent(weight=enemy_packet[1]))
        enemy.add_component(EnemyAIComponent())
        return enemy

    def get_random_direction(self):
        while True:
            x = random.choice([-1, 0, 1])
            y = random.choice([-1, 0, 1])
            if x != 0 or y != 0:  # Ensure movement
                return (x, y)

    def get_variable_enemy_packet(self) -> tuple[str, float, int, int, float]:
        # TODO: get base values from game settings and calculate variability here
        # texture_name, weight, size_w, size_h, speed
        mini = ("spider_1", 2, 50, 50, 90)
        med = ("spider_2", 3, 64, 64, 80)
        max = ("spider_3", 5, 80, 80, 70)
        return random.choice([mini, med, max])
