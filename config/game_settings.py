class GameSettings:
    def __init__(self):
        self.world_bounds = (1240, 680)

        self.protector_speed = 70
        self.protector_start = (0, 0)
        self.protector_size = (
            128,
            128,
        )  # TODO: have manifest read from here VS hard coding texture size
        self.protector_rotation_speed = 10
        self.protector_target_reach_distance = (
            2  # TODO: calculate distance threshold based protectors radius
        )
        self.protector_min_speed = 0  # Could be a small value to simulate drift
        self.protector_acceleration_rate = (
            90  # Adjust for how quickly the entity accelerates
        )
        self.protector_deceleration_rate = (
            60  # Adjust for how quickly the entity decelerates
        )
        self.protector_slowdown_distance = (
            50  # Start decelerating when within this range
        )
        self.protector_steering_force = 0.1  # Steer from current target to new target

        self.enemy_speed = 2
        self.enemy_size = (128, 128)

        self.heart_health = 10
        self.heart_start = (300, 300)
        self.heart_size = (256, 256)

        self.plant_health = 5
        self.screen_width = 800
        self.screen_height = 600
