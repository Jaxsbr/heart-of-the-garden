class GameSettings:
    def __init__(self):
        self.protector_speed = 70
        self.protector_start = (100, 100)
        self.protector_rotation_speed = 10
        self.protector_target_reach_distance = 10 # TODO: calculate distance threshold based protectors radius
        self.protector_min_speed = 0  # Could be a small value to simulate drift
        self.protector_acceleration_rate = 90  # Adjust for how quickly the entity accelerates
        self.protector_deceleration_rate = 80  # Adjust for how quickly the entity decelerates
        self.protector_slowdown_distance = 70  # Start decelerating when within this range
        self.protector_steering_force = 0.1 # Steer from current target to new target

        self.enemy_speed = 2

        self.heart_health = 10
        self.heart_start = (300, 300)

        self.plant_health = 5
        self.screen_width = 800
        self.screen_height = 600
