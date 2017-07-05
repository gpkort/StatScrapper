import unittest
import prostatscrapper
from prostatscrapper.prostatscrapper import ProStatScrapper, POSITION


class prostatscrapperTests(unittest.TestCase):
    def setUp(self):
        self.scrapper = ProStatScrapper()

    def test_get_core_number(self):
        self.scrapper = ProStatScrapper(True)
        self.assertEqual(4, self.scrapper.numberOfCores)

    def test_get_columns(self):
        columns = self.scrapper.get_columns(POSITION.RUNNINGBACK)
        self.assertIsNotNone(columns, 'Columns are none')
        self.assertEqual(24, len(columns), 'RB column length incorrect')

        columns = self.scrapper.get_columns(POSITION.QUARTERBACK)
        self.assertIsNotNone(columns, 'Columns are none')
        self.assertEqual(26, len(columns), 'QB column length incorrect')

        columns = self.scrapper.get_columns(POSITION.WIDE_RECEIVER)
        self.assertIsNotNone(columns, 'Columns are none')
        self.assertEqual(25, len(columns), 'WR column length incorrect')

        columns = self.scrapper.get_columns(POSITION.NONE)
        self.assertIsNone(columns, 'Columns are not none')

    def test_get_all_columns(self):
        col_dict = self.scrapper.get_all_columns()
        self.assertIsNotNone(col_dict)
        self.assertEqual(len(POSITION)-1, len(col_dict), 'Dictionary length incorrect')

    # def test_get_position(self):
    #     players_dict = self.scrapper.get_all_players_by_position(POSITION.RUNNINGBACK)
    #     self.assertIsNotNone(players_dict, 'All positions are None')
    #     self.assertGreater(len(players_dict), 0, "Empty player/pos dataset")
    #     print(players_dict.tail())

    def test_get_players_dataset(self):
        ds1 = self.scrapper.get_players_dataset(POSITION.QUARTERBACK, 'Z')
        self.assertIsNotNone(ds1, "Null dataset")
        self.assertTrue(len(ds1) > 0, "Empty data set")

        ds2 = self.scrapper.get_players_dataset(POSITION.QUARTERBACK, 'zebra')
        self.assertIsNotNone(ds2, "Null dataset")
        self.assertEqual(len(ds2), len(ds2), "Empty data set")

    def test_get_runningbacks_dataset(self):
        rbds = self.scrapper.get_players_by_position_and_letter(POSITION.RUNNINGBACK, 'I')
        self.assertGreater(len(rbds), 0, "Empty player dataset")
        print(rbds.head())

    def test_get_quarterbacks_dataset(self):
        qbds = self.scrapper.get_players_by_position_and_letter(POSITION.QUARTERBACK, 'Z')
        self.assertGreater(len(qbds), 0, "Empty player dataset")
        print(qbds.head())

    def test_get_receivers_dataset(self):
        wrds = self.scrapper.get_players_by_position_and_letter(POSITION.WIDE_RECEIVER, 'Z')
        self.assertGreater(len(wrds), 0, "Empty receiver player dataset")
        print(wrds.head())

    def test_get_te_dataset(self):
        wrds = self.scrapper.get_players_by_position_and_letter(POSITION.TIGHT_END, 'G')
        self.assertGreater(len(wrds), 0, "Empty receiver player dataset")
        print(wrds.head())
