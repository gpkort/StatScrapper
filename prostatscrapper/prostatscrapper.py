from enum import Enum
from bs4 import BeautifulSoup
import pandas as pd
import requests


class POSITION(Enum):
    NONE = 0,
    RUNNINBACK = 1


STANDARD_URL = 'http://www.pro-football-reference.com'
PLAYERS = '/players'
RUNNINGBACK = 'rb'
SLASH = '/'


class ProStatScrapper(object):
    __PLAYER_DICTIONARY = {POSITION.RUNNINBACK: 'RB'}

    __rb_dataset = None

    def __init__(self, path=None):
        self.url = STANDARD_URL if path is None else path

    def get_all(self):
        pass

    def get_all_by_position(self, position):
        return None

    def get_all_by_last(self, letter):
        pass

    def get_by_name(self, name, position=POSITION.NONE):
        pass

    def get_all_columns(self):
        column_dict = {}

        for pos in POSITION:
            if pos == POSITION.NONE:
                continue
            else:
                column_dict[pos] = self.get_columns(pos)

            return column_dict

    def get_columns(self, position):
        if position == POSITION.RUNNINBACK:
            return ['id', 'name', 'year', 'g', 'gs', 'rush_att', 'rush_yds', 'rush_td', 'rush_long',
                    'rush_yds_per_att', 'rush_yds_per_g', 'rush_att_per_g', 'rec', 'rec_yds',
                    'rec_yds_per_rec', 'rec_td', 'rec_long', 'rec_per_g', 'rec_yds_per_g',
                    'yds_from_scrimmage', 'rush_receive_td', 'fumbles']
        else:
            return None

    def get_players_dataset(self, position, letter):
        req = requests.get("http://www.pro-football-reference.com" + '/' + PLAYERS + '/' + letter)
        soup = BeautifulSoup(req.text, "lxml")
        players = soup.find_all('div', {'class': 'section_content'})
        player_df = pd.DataFrame(columns=('link', 'name'))
        i = 0
        pos = '(' + ProStatScrapper.__PLAYER_DICTIONARY[position] + ')'

        for div in players:
            for line in div.find_all('p'):
                if pos in line.text:
                    link = line.find('a')
                    player_df.loc[i] = [str(link['href']), link.text]
                    i += 1

        return player_df

    def __str__(self):
        return str.format('Pro football stats {}', self.url)
