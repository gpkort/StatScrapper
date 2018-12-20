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
YEARS = 'years'

FIRST_YEAR = 1950
LAST_YEAR = 2017

ALL_PRO_STRING = 'all_pro_string'

TEAM_DICT_KEYS = ['team_name', 'team_url', 'year_min', 'year_max',
                  'years_playoffs', 'championships', 'championships_super_bowl',
                  'championships_conference', 'championships_division']

TEAM_YEAR_DICT_KEYS = ['year_id', 'team', 'team_url', 'wins', 'losses', 'ties',
                       'div_finish', 'points', 'points_opp', 'points_diff',
                       'coaches', 'coaches_url', 'rank_off_pts', 'rank_off_yds',
                       'rank_takeaway_giveaway', 'teams_in_league']

YEAR_PLAYOFF_KEYS = ['team', 'team_url', 'seed', 'conference']

DATA_DELIMITER = '|'
