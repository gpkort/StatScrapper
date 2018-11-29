from enum import Enum

class POSITION(Enum):
    """
    An enumerator to define player positions

    """
    NONE = 0,
    RUNNING_BACK = 1,
    QUARTERBACK = 2,
    WIDE_RECEIVER = 3,
    TIGHT_END = 4


STANDARD_URL = 'http://www.pro-football-reference.com'
PLAYERS = '/players'
SLASH = '/'