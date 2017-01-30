from enum import Enum
from bs4 import BeautifulSoup
import pandas as pd
import requests
from string import ascii_lowercase


class POSITION(Enum):
    NONE = 0,
    RUNNINGBACK = 1,
    QUARTERBACK = 2,
    WIDE_RECEIVER = 3,
    TIGHT_END = 4


STANDARD_URL = 'http://www.pro-football-reference.com'
PLAYERS = '/players'
SLASH = '/'


class ProStatScrapper(object):
    __PLAYER_DICTIONARY = {POSITION.RUNNINGBACK: 'RB',
                           POSITION.QUARTERBACK: 'QB',
                           POSITION.WIDE_RECEIVER: 'WR',
                           POSITION.TIGHT_END: 'TE'
                           }


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
        if position == POSITION.RUNNINGBACK:
            return ['id', 'name', 'team', 'age', 'year', 'g', 'gs', 'rush_att', 'rush_yds',
                    'rush_td', 'rush_long', 'rush_yds_per_att', 'rush_yds_per_g',
                    'rush_att_per_g', 'rec', 'rec_yds', 'rec_yds_per_rec', 'rec_td',
                    'rec_long', 'rec_per_g', 'rec_yds_per_g', 'yds_from_scrimmage',
                    'rush_receive_td', 'fumbles']

        elif position == POSITION.QUARTERBACK:
            return ['id', 'name', 'team', 'age', 'year', 'g', 'gs', 'pass_cmp', 'pass_att',
                    'pass_cmp_perc', 'pass_yds', 'pass_td', 'pass_td_perc', 'pass_int',
                    'pass_int_perc', 'pass_long', 'pass_yds_per_att', 'pass_adj_yds_per_att',
                    'pass_yds_per_cmp', 'pass_yds_per_g', 'pass_rating', 'pass_sacked',
                    'pass_sacked_yds', 'pass_net_yds_per_att', 'pass_adj_net_yds_per_att',
                    'pass_sacked_perc']

        elif position == POSITION.WIDE_RECEIVER or  position == POSITION.TIGHT_END:
            return ['id', 'name', 'age', 'year', 'team', 'g', 'gs', 'rec', 'rec_yds',
                    'rec_yds_per_rec', 'rec_td', 'rec_long', 'rec_per_g', 'rec_yds_per_g',
                    'catch_pct', 'rush_att', 'rush_yds', 'rush_td', 'rush_long',
                    'rush_yds_per_att', 'rush_yds_per_g', 'rush_att_per_g', 'yds_from_scrimmage',
                    'rush_receive_td', 'fumbles']
        else:
            return None

    def get_all_players_by_position(self, position):
        ds_list = []

        for l in ascii_lowercase:
            player_df = self.get_players_dataset(position, l)

            if position == POSITION.RUNNINGBACK:
                print('Getting th players that begin with ' + l)
                ds_list.append(self.get_runningbacks_dataset(player_df))

        return pd.concat(ds_list)

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

    def get_quarterbacks_dataset(self, qb_dataset):
        i = 0
        years = pd.DataFrame(columns=self.get_columns(POSITION.QUARTERBACK))

        for index, prow in qb_dataset.iterrows():
            print('Retrieving quarterback ' + prow['name'])

            url = STANDARD_URL + prow['link']
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
                if row.has_attr('id') and 'passing' in row['id']:
                    year = row.find('th').text[:4]
                    g = row.find('td', {'data-stat': 'g'}).text
                    gs = row.find('td', {'data-stat': 'gs'}).text
                    pass_cmp = row.find('td', {'data-stat': 'pass_cmp'}).text
                    pass_att = row.find('td', {'data-stat': 'pass_att'}).text
                    pass_cmp_perc = row.find('td', {'data-stat': 'pass_cmp_perc'}).text
                    pass_yds = row.find('td', {'data-stat': 'pass_yds'}).text
                    pass_td = row.find('td', {'data-stat': 'pass_td'}).text
                    pass_td_perc = row.find('td', {'data-stat': 'pass_td_perc'}).text
                    pass_int_perc = row.find('td', {'data-stat': 'pass_int_perc'}).text
                    pass_int = row.find('td', {'data-stat': 'pass_int'}).text
                    pass_long = row.find('td', {'data-stat': 'pass_long'}).text
                    pass_yds_per_att = row.find('td', {'data-stat': 'pass_yds_per_att'}).text
                    pass_adj_yds_per_att = row.find('td', {'data-stat': 'pass_adj_yds_per_att'}).text
                    pass_yds_per_cmp = row.find('td', {'data-stat': 'pass_yds_per_cmp'}).text
                    pass_yds_per_g = row.find('td', {'data-stat': 'pass_yds_per_g'}).text
                    pass_rating = row.find('td', {'data-stat': 'pass_rating'}).text
                    pass_sacked = row.find('td', {'data-stat': 'pass_sacked'}).text
                    pass_sacked_yds = row.find('td', {'data-stat': 'pass_sacked_yds'}).text
                    pass_net_yds_per_att = row.find('td', {'data-stat': 'pass_net_yds_per_att'}).text
                    pass_adj_net_yds_per_att = row.find('td', {'data-stat': 'pass_adj_net_yds_per_att'}).text
                    pass_sacked_perc = row.find('td', {'data-stat': 'pass_sacked_perc'}).text
                    age = row.find('td', {'data-stat': 'age'}).text
                    team = row.find('td', {'data-stat': 'team'}).text

                    years.loc[i] = [pid, prow['name'], team, age, year, g, gs, pass_cmp, pass_att,
                                    pass_cmp_perc, pass_yds, pass_td, pass_td_perc, pass_int,
                                    pass_int_perc, pass_long, pass_yds_per_att, pass_adj_yds_per_att,
                                    pass_yds_per_cmp, pass_yds_per_g, pass_rating, pass_sacked,
                                    pass_sacked_yds, pass_net_yds_per_att, pass_adj_net_yds_per_att,
                                    pass_sacked_perc]
                    i += 1

        return years

    def get_runningbacks_dataset(self, rb_dataset):
        i = 0
        years = pd.DataFrame(columns=self.get_columns(POSITION.RUNNINGBACK))

        for index, prow in rb_dataset.iterrows():
            print('Retrieving running back ' + prow['name'])

            url = STANDARD_URL + prow['link']
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
                if row.has_attr('id') and 'rushing_and_receiving' in row['id']:
                    year = row.find('th').text[:4]
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
                    age = row.find('td', {'data-stat': 'age'}).text
                    team = row.find('td', {'data-stat': 'team'}).text
                    years.loc[i] = [pid, prow['name'], team, age, year, g, gs, rush_att, rush_yds, rush_td, rush_long,
                                    rush_yds_per_att, rush_yds_per_g, rush_att_per_g, rec, rec_yds, rec_yds_per_rec,
                                    rec_td, rec_long, rec_per_g, rec_yds_per_g, yds_from_scrimmage,
                                    rush_receive_td, fumbles]
                    i += 1

        return years

    def get_catching_dataset(self, wr_dataset, position):
        i = 0
        years = pd.DataFrame(columns=self.get_columns(position))

        for index, prow in wr_dataset.iterrows():
            message = 'Wide Receiver' if position == POSITION.WIDE_RECEIVER else 'Tight End'
            print('Retrieving ' + message + ": " + prow['name'])

            url = STANDARD_URL + prow['link']
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
                if row.has_attr('id') and 'receiving_and_rushing' in row['id']:
                    year = row.find('th').text[:4]
                    g = row.find('td', {'data-stat': 'g'}).text
                    gs = row.find('td', {'data-stat': 'gs'}).text

                    rec = row.find('td', {'data-stat': 'rec'}).text
                    rec_yds = row.find('td', {'data-stat': 'rec_yds'}).text
                    rec_yds_per_rec = row.find('td', {'data-stat': 'rec_yds_per_rec'}).text
                    rec_td = row.find('td', {'data-stat': 'rec_td'}).text
                    rec_long = row.find('td', {'data-stat': 'rec_long'}).text
                    rec_per_g = row.find('td', {'data-stat': 'rec_per_g'}).text
                    rec_yds_per_g = row.find('td', {'data-stat': 'rec_yds_per_g'}).text
                    catch_pct = row.find('td', {'data-stat': 'catch_pct'}).text
                    rush_att = row.find('td', {'data-stat': 'rush_att'}).text
                    rush_yds = row.find('td', {'data-stat': 'rush_yds'}).text
                    rush_long = row.find('td', {'data-stat': 'rush_long'}).text
                    rush_yds_per_att = row.find('td', {'data-stat': 'rush_yds_per_att'}).text
                    rush_yds_per_g = row.find('td', {'data-stat': 'rush_yds_per_g'}).text
                    rush_att_per_g = row.find('td', {'data-stat': 'rush_att_per_g'}).text
                    yds_from_scrimmage = row.find('td', {'data-stat': 'yds_from_scrimmage'}).text
                    rush_td = row.find('td', {'data-stat': 'rush_td'}).text
                    rush_receive_td = row.find('td', {'data-stat': 'rush_receive_td'}).text
                    fumbles = row.find('td', {'data-stat': 'fumbles'}).text
                    age = row.find('td', {'data-stat': 'age'}).text
                    team = row.find('td', {'data-stat': 'team'}).text

                    years.loc[i] = [pid, prow['name'], age, year, team, g, gs, rec, rec_yds, rec_yds_per_rec,
                                    rec_td, rec_long,  rec_per_g, rec_yds_per_g, catch_pct, rush_att,
                                    rush_yds, rush_td, rush_long, rush_yds_per_att, rush_yds_per_g,
                                    rush_att_per_g, yds_from_scrimmage, rush_receive_td, fumbles]
                    i += 1

        return years

    def __str__(self):
        return str.format('Pro football stats {}', self.url)


