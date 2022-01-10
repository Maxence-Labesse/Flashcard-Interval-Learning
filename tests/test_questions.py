"""questions module tests

"""
import unittest
import pandas as pd
from flashcards.utils.questions import *

d_topic_data = {
    'ID_topic': [1, 2, 3],
    'topic': ['Topic_1', 'Topic_2', 'Topic_3']
}

d_questions_data = {
    'ID_question': [1, 2, 3, 4, 5],
    'ID_topic': [1, 1, 1, 2, 3],
    'label': ['Label_1', 'Label_2', 'Label_3', 'Label_4', 'Label_5'],
    'link': ['Link_1', 'Link_2', 'Link_3', 'Link_4', 'Link_5'],
    'box': [1, 1, 4, 2, 3]
}

df_topic = pd.DataFrame.from_dict(d_topic_data)
df_questions = pd.DataFrame.from_dict(d_questions_data)


class TestUtils(unittest.TestCase):

    def test_forward_box(self):
        self.assertEqual(forward_box(1), 2, "should be 2")
        self.assertEqual(forward_box(4), 4, "should be 4")

    def test_backward_box(self):
        self.assertEqual(backward_box(1), 1, "should be 1")
        self.assertEqual(backward_box(4), 3, "should be 3")

    def test_filter_dataframe(self):
        df_filtered_1 = filter_dataframe(df_questions, 'ID_topic', 1)
        df_filtered_2 = filter_dataframe(df_questions, 'label', ['Label_2', 'Label_3'])
        self.assertEqual(df_filtered_1.shape[0], 3, "should be 3")
        self.assertEqual(df_filtered_2.shape[0], 2, "should be 2")

    def test_pick_random_topic(self):
        random_topic_id, topic_name = pick_random_topic(df_topic)
        topic_row = df_topic.loc[df_topic["ID_topic"] == random_topic_id]
        topic_row_name = topic_row["topic"].values[0]
        self.assertIn(random_topic_id, [1, 2, 3], "should be in [1, 2, 3]")
        self.assertEqual(topic_name, topic_row_name, "should be the same topic")


question = Question(df_questions, df_topic, name="test_question")


class TestQuestion(unittest.TestCase):

    def test_init(self):
        self.assertEqual(question.name, "test_question", "should be test_question")
        self.assertIsInstance(question.ID, int)
        self.assertIsInstance(question.label, str)
        self.assertIsInstance(question.topic, str)
        self.assertIsInstance(question.link, str)
        self.assertTrue(1 <= question.box <= 4)

    def test_update_box(self):
        for i in range(10):
            question.update_box(True)
            self.assertTrue(1 <= question.box <= 4)
        self.assertEqual(question.box, 4)

        for i in range(10):
            question.update_box(False)
            self.assertTrue(1 <= question.box <= 4)
        self.assertEqual(question.box, 1)

    def test_save_box_in_database(self):
        """TODO"""
        pass


if __name__ == '__main__':
    unittest.main()
