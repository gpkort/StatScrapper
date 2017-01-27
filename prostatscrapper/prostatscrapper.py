from enum import Enum
from bs4 import BeautifulSoup
import pandas as pd
import requests
from string import ascii_lowercase



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
            return ['id', 'name', 'team', 'age', 'year', 'g', 'gs', 'rush_att', 'rush_yds', 'rush_td', 'rush_long',
                    'rush_yds_per_att', 'rush_yds_per_g', 'rush_att_per_g', 'rec', 'rec_yds',
                    'rec_yds_per_rec', 'rec_td', 'rec_long', 'rec_per_g', 'rec_yds_per_g',
                    'yds_from_scrimmage', 'rush_receive_td', 'fumbles']
        else:
            return None

    def get_all_players_by_position(self, position):
        ds_list = []

        for l in ascii_lowercase:
            player_df = self.get_players_dataset(position, l)

            if position == POSITION.RUNNINBACK:
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

    def get_runningbacks_dataset(self, rb_dataset):
        i = 0
        years = pd.DataFrame(columns=self.get_columns(POSITION.RUNNINBACK))

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

    def __str__(self):
        return str.format('Pro football stats {}', self.url)

"""
<table class="row_summable sortable stats_table" id="passing" data-cols-to-freeze=2><caption>Passing Table</caption>

<tr id="passing.1979" class="full_table" >
 <th scope="row" class="left " data-stat="year_id" ><a href="/years/1979/">1979</a></th>
 <td class="right " data-stat="age" >23</td>
 <td class="left " data-stat="team" ><a href="/teams/sfo/1979.htm" title="San Francisco 49ers">SFO</a></td>
 <td class="left " data-stat="pos" >qb</td>
 <td class="right " data-stat="uniform_number" >16</td>
 <td class="right " data-stat="g" >16</td>
 <td class="right " data-stat="gs" >1</td>
 <td class="right " data-stat="qb_rec" csk="0.00000" >0-1-0</td>
 <td class="right " data-stat="pass_cmp" >13</td>
 <td class="right " data-stat="pass_att" >23</td>
 <td class="right " data-stat="pass_cmp_perc" >56.5</td>
 <td class="right " data-stat="pass_yds" >96</td>
 <td class="right " data-stat="pass_td" >1</td>
 <td class="right " data-stat="pass_td_perc" >4.3</td>
 <td class="right " data-stat="pass_int" >0</td>
 <td class="right " data-stat="pass_int_perc" >0.0</td>
 <td class="right " data-stat="pass_long" >18</td>
 <td class="right " data-stat="pass_yds_per_att" >4.2</td>
 <td class="right " data-stat="pass_adj_yds_per_att" >5.0</td>
 <td class="right " data-stat="pass_yds_per_cmp" >7.4</td>
 <td class="right " data-stat="pass_yds_per_g" >6.0</td>
 <td class="right " data-stat="pass_rating" >81.1</td>
 <td class="right " data-stat="pass_sacked" >0</td>
 <td class="right " data-stat="pass_sacked_yds" >0</td>
 <td class="right " data-stat="pass_net_yds_per_att" >4.17</td>
 <td class="right " data-stat="pass_adj_net_yds_per_att" >5.04</td>
 <td class="right " data-stat="pass_sacked_perc" >0.0</td>
 <td class="right " data-stat="comebacks" ></td>
 <td class="right " data-stat="gwd" ></td>
 <td class="right " data-stat="av" >0</td>
</tr>
"""