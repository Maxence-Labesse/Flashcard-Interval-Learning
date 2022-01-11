"""update_database module tests

"""
import unittest
from flashcards.update_database import *

path_database = "test_database.db"

# open connexion
conn = sqlite3.connect(path_database)

# create database tables
create_database(conn)

# get tables columns
questions_cols = pd.read_sql_query("SELECT * from {}".format('questions'), conn).columns.tolist()
topics_cols = pd.read_sql_query("SELECT * from {}".format('topics'), conn).columns.tolist()

c = conn.cursor()
c.execute("""DROP TABLE 'questions' """)
c.execute("""DROP TABLE 'topics' """)

conn.commit()
conn.close()


class TestUpdateDatabase(unittest.TestCase):

    def test_create_database(self):
        self.assertEqual(questions_cols, ['ID_question', 'ID_topic', 'label', 'link', 'box'])
        self.assertEqual(topics_cols, ['ID_topic', 'topic'])

    def test_update_database(self):
        """TODO"""
        pass
