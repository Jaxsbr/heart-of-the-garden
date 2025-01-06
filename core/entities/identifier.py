from core.attack_priority import AttackPriority
from core.components.attackable_component import AttackableComponent
from core.components.controllable_component import ControllableComponent
from core.components.movement_component import MovementComponent
from core.entities.entity import Entity


def is_protector_entity(entity: Entity) -> bool:
    # Protector is the only controllable entitty
    return entity.get_component(ControllableComponent) is not None


def is_heart_entity(entity: Entity) -> bool:
    # Heart has the highest attack priority of all attackable entities
    attackable = entity.get_component(AttackableComponent)
    return attackable is not None and attackable.attack_priority == AttackPriority.HIGH


def is_plant_entity(entity: Entity) -> bool:
    # Plant has medium attack priority
    attackable = entity.get_component(AttackableComponent)
    return (
        attackable is not None and attackable.attack_priority == AttackPriority.MEDIUM
    )


def is_moving_entity(entity: Entity) -> bool:
    return entity.get_component(MovementComponent) is not None
