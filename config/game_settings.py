class GameSettings:
    def __init__(self):
        self.world_bounds = (1240, 680)

        self.protector_speed = 120
        self.protector_start = (0, 0)
        self.protector_size = (
            64,
            64,
        )  # TODO: have manifest read from here VS hard coding texture size
        self.protector_rotation_speed = 10
        self.protector_target_reach_distance = 10  # TODO: calculate
        self.protector_min_speed = 0
        self.protector_acceleration_rate = 220
        self.protector_deceleration_rate = 220
        self.protector_slowdown_distance = 32
        self.protector_steering_force = 0.1
        self.protector_weight = 15

        self.enemy_size = (
            64,
            64,
        )  # TODO: have manifest read from here VS hard coding texture size
        self.enemy_target_reach_distance = 2  # TODO: calculate
        self.enemy_rotation_speed = 15
        self.enemy_speed = 70
        self.enemy_min_speed = 0
        self.enemy_acceleration_rate = 120
        self.enemy_deceleration_rate = 120
        self.enemy_slowdown_distance = 50
        self.enemy_steering_force = 0.05
        self.enemy_size = (64, 64)
        self.enemy_weight = 3

        self.heart_health = 10
        self.heart_start = (300, 300)
        self.heart_size = (128, 128)
        self.heart_weight = 25

        self.plant_health = 5
        self.screen_width = 800
        self.screen_height = 600
