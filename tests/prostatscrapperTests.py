import unittest
import prostatscrapper
from prostatscrapper.prostatscrapper import ProStatScrapper, POSITION


class prostatscrapperTests(unittest.TestCase):
    def setUp(self):
        self.scrapper = ProStatScrapper()

    def test_get_columns(self):
        columns = self.scrapper.get_columns(POSITION.RUNNINBACK)
        self.assertIsNotNone(columns, 'Columns are none')
        self.assertEqual(22, len(columns), 'RB column length incorrect')

        columns = self.scrapper.get_columns(POSITION.NONE)
        self.assertIsNone(columns, 'Columns are not none')

    def test_get_all_columns(self):
        col_dict = self.scrapper.get_all_columns()
        self.assertIsNotNone(col_dict)
        self.assertEqual(len(POSITION)-1, len(col_dict), 'Dictionary length incorrect')

    def test_get_position(self):
        players_dict = self.scrapper.get_all_by_position(POSITION.RUNNINBACK)
        self.assertIsNone(players_dict, 'All positions are None')


