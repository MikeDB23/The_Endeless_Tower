from enum import Enum

class Behavior(Enum):
    PLAYABLE = 1
    BASIC = 2

class AttackType(Enum):
    PHYSICAL = 1
    MAGICAL = 2
    HEAL = 3

class HitType(Enum):
    NORMAL = 1
    FAILED = 2
    CRIT = 3

class Element(Enum):
    HEAL = 1
    PHYSICAL = 2
    FIRE = 3