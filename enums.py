from enum import Enum, auto


class Turn(Enum):
    PLAYER = auto()
    DEALER = auto()

class BulletType(Enum):
    LIVE_AMMO = auto()
    BLANK = auto()

class MovementOption(Enum):
    NONE = auto()
    SHOT_OPPOSITE = auto()
    SHOT_SELF = auto()

