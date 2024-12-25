# Gradual Direction Adjustment with Lerp

To ensure smooth and realistic direction changes for game entities, **linear interpolation (lerp)** is used to gradually adjust the current angle toward the target angle. This avoids abrupt direction changes and improves visual realism.

- **What is Lerp?**
  Lerp (linear interpolation) is a method to smoothly transition between two values over time by incrementally adjusting the current value toward the target value.

- **How it Works in this System:**
  - The current angle adjusts incrementally toward the target angle using a fixed rotation speed (degrees per update cycle).
  - The shortest rotation path (clockwise or counterclockwise) is automatically chosen to avoid unnecessary full-circle rotations.
  - A small step size ensures the rotation appears smooth and natural.

- **Key Advantages:**
  - Prevents abrupt, unrealistic changes in direction.
  - Provides a configurable rotation speed for fine-tuned control over visual behavior.
  - Automatically handles angle wrapping between 0° and 360°.

This approach is implemented in the `_lerp_angle` function within the `DirectionalRotationSystem`.
