from dataclasses import dataclass


@dataclass
class AttackEncounter:
    enemy_id: str
    attackable_id: str
