"""date_utils module tests

"""
import unittest
from flashcards.utils.date_utils import *
import datetime

date_str = '2022-01-21'
date_datetime = datetime.datetime(2022, 1, 21)
date_date = datetime.date(2022, 1, 21)


class TestDateUtils(unittest.TestCase):

    def test_raw_dates(self):
        self.assertNotEqual(date_str, date_datetime)
        self.assertNotEqual(date_date, date_datetime)
        self.assertNotEqual(date_str, date_date)

    def test_to_datetime_date(self):
        self.assertIsInstance(to_datetime_date(date_str), datetime.date)
        self.assertIsInstance(to_datetime_date(date_datetime), datetime.date)
        self.assertIsInstance(to_datetime_date(date_date), datetime.date)

    def test_test_same_dates(self):
        self.assertTrue(test_same_dates(date_str, date_datetime))
        self.assertTrue(test_same_dates(date_date, date_datetime))
        self.assertTrue(test_same_dates(date_str, date_date))
