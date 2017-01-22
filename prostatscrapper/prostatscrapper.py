from enum import Enum

class POSITION(Enum):
    NONE = 0,
    RUNNINBACK = 1

STANDARD_URL = 'http://www.pro-football-reference.com/players'
RUNNINGBACK = 'rb'
SLASH = '/'
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
           't', 'u', 'v', 'w', 'x', 'y', 'z']


class statscrapper(object):
    __PLAYER_DICTIONARY = {POSITION.RUNNINBACK: 'rb'}

    __rb_dataset = None

    def __init__(self, path=None):
        self.url =  STANDARD_URL if path is None else path

    def get_all(self):
        pass

    def get_all_by_position(self, position):
        pass

    def get_all_by_last(self, letter):
        pass

    def get_by_name(self, name, position=POSITION.NONE):
        pass

    def __str__(self):
        return str.format('Pro footbal stats {}', self.url)


