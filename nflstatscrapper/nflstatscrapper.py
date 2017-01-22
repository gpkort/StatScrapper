from enum import Enum

class POSITION(Enum):
    NONE = 0,
    RUNNINBACK = 1

STANDARD_URL = 'http://www.pro-football-reference.com/players'
RUNNINGBACK = 'rb'
SLASH = '/'
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
           't', 'u', 'v', 'w', 'x', 'y', 'z']

PLAYER_DICTIONARY = {POSITION.RUNNINBACK: 'rb'}


class statscrapper(object):

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


