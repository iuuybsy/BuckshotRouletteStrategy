from enum import Enum, auto


class Turn(Enum):
    PLAYER = auto()
    DEALER = auto()

class BulletType(Enum):
    LIVE_AMMO = auto()
    BLANK = auto()

class MovementOption(Enum):
    SHOT_OPPOSITE = auto()
    SHOT_SELF = auto()

class MovementResult(Enum):
    HAVE_GUTS = auto()
    SUICIDE = auto()
    SPECTACLE = auto()
    KILL = auto()

