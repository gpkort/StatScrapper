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
PROBOWL_PAGE = "years/{}/probowl.htm"
TEAMS = 'teams'


FIRST_YEAR = 1950
LAST_YEAR = 2017

ALL_PRO_STRING = 'all_pro_string'