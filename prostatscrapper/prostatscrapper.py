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
        req = requests.get(STANDARD_URL + '/' + PLAYERS + '/' + letter.upper())
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

    def get_runningbacks_dataset(self, rb_dataset):
        i = 0
        years = pd.DataFrame(columns=self.get_columns(POSITION.RUNNINBACK))

        for index, prow in rb_dataset.iterrows():
            url = STANDARD_URL + prow['link']
            print('URL = ' + url)
            req = requests.get(url)
            soup = BeautifulSoup(req.text, "lxml")
            stats_overall = soup.find_all('table', {'class': 'row_summable sortable stats_table'})
            if len(stats_overall) == 0:
                continue

            stats_table = stats_overall[0].find_all('tbody')
            if len(stats_table) == 0:
                continue

            last_slash_idx = url.rfind('/') + 1
            last_dot_idx = url.rfind('.')
            pid = url[last_slash_idx: last_dot_idx]

            for row in stats_table[0].find_all('tr'):
                if 'id' in row and 'rushing_and_receiving' in row['id']:
                    year = row.find('th').text[:4]
                    print('Year = ' + year)

                    g = 0
                    g = row.find('td', {'data-stat': 'g'}).text

                    gamestarts = row.find('td', {'data-stat': 'gs'})
                    gs = gamestarts.text
                    rush_att = row.find('td', {'data-stat': 'rush_att'}).text
                    rush_yds = row.find('td', {'data-stat': 'rush_yds'}).text
                    rush_td = row.find('td', {'data-stat': 'rush_td'}).text
                    rl = row.find('td', {'data-stat': 'rush_long'})
                    rush_long = rl.text

                    rush_yds_per_att = row.find('td', {'data-stat': 'rush_yds_per_att'}).text
                    rush_yds_per_g = row.find('td', {'data-stat': 'rush_yds_per_g'}).text
                    rush_att_per_g = row.find('td', {'data-stat': 'rush_att_per_g'}).text
                    rec = row.find('td', {'data-stat': 'rec'}).text
                    rec_yds = row.find('td', {'data-stat': 'rec_yds'}).text
                    rec_yds_per_rec = row.find('td', {'data-stat': 'rec_yds_per_rec'}).text
                    rec_td = row.find('td', {'data-stat': 'rec_td'}).text
                    rec_long = row.find('td', {'data-stat': 'rec_long'}).text
                    rec_per_g = row.find('td', {'data-stat': 'rec_per_g'}).text
                    rec_yds_per_g = row.find('td', {'data-stat': 'rec_yds_per_g'}).text
                    yds_from_scrimmage = row.find('td', {'data-stat': 'yds_from_scrimmage'}).text
                    rush_receive_td = row.find('td', {'data-stat': 'rush_receive_td'}).text
                    fumbles = row.find('td', {'data-stat': 'fumbles'}).text
                    years.loc[i] = [pid, prow['name'], year, g, gs, rush_att, rush_yds, rush_td, rush_long,
                                    rush_yds_per_att, rush_yds_per_g, rush_att_per_g, rec, rec_yds, rec_yds_per_rec,
                                    rec_td, rec_long, rec_per_g, rec_yds_per_g, yds_from_scrimmage,
                                    rush_receive_td, fumbles]
                    i += 1

        return years

    def __str__(self):
        return str.format('Pro football stats {}', self.url)
