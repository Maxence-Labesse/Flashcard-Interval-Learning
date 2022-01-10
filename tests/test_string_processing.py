"""string_processing module tests

"""
import unittest
from flashcards.utils.string_processing import *


class TestStringProcessing(unittest.TestCase):

    def test_concat_key_value(self):
        d_test = {'key_1': 'value_1', 'key_2': 'value_2'}
        self.assertEqual(concat_key_value(d_test), ['key_1 value_1', 'key_2 value_2'])

    def test_is_str(self):
        self.assertTrue(is_str('txt'))
        self.assertFalse(is_str(1))

    def test_to_str(self):
        self.assertEqual(to_str(1, quote_str=False), "1")
        self.assertEqual(to_str(1, quote_str=True), "1")
        self.assertEqual(to_str("txt", quote_str=False), "txt")
        self.assertEqual(to_str("txt", quote_str=True), "\'txt\'")

    def test_concat_list(self):
        l_test = [1, "txt_1", 2, "txt_2"]
        self.assertEqual(concat_list(l_test, sep=',', quote_str=False), "1,txt_1,2,txt_2")
        self.assertEqual(concat_list(l_test, sep=';', quote_str=True), "1;\'txt_1\';2;\'txt_2\'")
        self.assertNotEqual(concat_list(l_test, sep=';', quote_str=True), "1\'txt_1\';2;\'txt_2\'")

    def test_prepare_data_for_db_insert(self):
        l_data = [1, "txt_1", 2, "txt_2"]
        self.assertEqual(prepare_data_for_db_insert(l_data, primary_key=False),
                         "(1,\'txt_1\',2,\'txt_2\')")
        self.assertEqual(prepare_data_for_db_insert(l_data, primary_key=True),
                         "(NULL, 1,\'txt_1\',2,\'txt_2\')")
