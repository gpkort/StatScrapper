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
        players_dict = self.scrapper.get_all_players_by_position(POSITION.RUNNINBACK)
        self.assertIsNotNone(players_dict, 'All positions are None')
        self.assertGreater(len(players_dict), 0, "Empty player/pos dataset")
        print(players_dict.tail())

    def test_get_players_dataset(self):
        ds = self.scrapper.get_players_dataset(POSITION.RUNNINBACK, 'A')
        self.assertIsNotNone(ds, "Null dataset")
        self.assertTrue(len(ds) > 0, "Empty data set")

    def test_get_runningbacks_dataset(self):
        ds = self.scrapper.get_players_dataset(POSITION.RUNNINBACK, 'I')
        rbds = self.scrapper.get_runningbacks_dataset(ds)
        self.assertGreater(len(rbds), 0, "Empty player dataset")
        print(rbds.head())



