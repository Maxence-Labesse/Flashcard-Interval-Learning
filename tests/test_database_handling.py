"""database_handling module tests

"""
import unittest
from flashcards.utils.database_handling import *

path_database = "test_database.db"

d_var_table_1 = {
    "var_id": 'INTEGER PRIMARY KEY AUTOINCREMENT',
    "var_1": "int",
    "var_2": "txt"
}

d_var_table_2 = {
    "var_1": "int",
    "var_2": "txt"
}

# We create table_1 in the database using db_conn
db_conn(path_database, create_table_in_db, table_name="table_1", d_var_types=d_var_table_1, drop=False)

# open connexion
conn = sqlite3.connect(path_database)
c = conn.cursor()

# test that table_1 exist
c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='table_1'""")
test_table_1_exist = c.fetchone()

# We create table_2 in the database
create_table_in_db(conn, "table_2", d_var_table_2, drop=False)
c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='table_2'""")
test_table_2_exist = c.fetchone()

# We insert data in table 1 and 2
insert_in_db_table(conn, "table_1", [1, "text"], primary_key=True)
c.execute("""SELECT * from table_1""")
test_inserted_values_1 = c.fetchone()

insert_in_db_table(conn, "table_2", [1, "text"], primary_key=False)
c.execute("""SELECT * from table_2""")
test_inserted_values_2 = c.fetchone()

# We delete row of table 1
delete_from_db_table(conn, 'table_1', rowid=1)
c.execute("""SELECT * from table_1""")
test_delete_values_1 = c.fetchone()

# We import table 2 in a dataframe
df_table_2 = db_table_to_dataframe(conn, ['table_2'])
d_table_2_infos = get_db_table_infos(conn, 'table_2')

# drop tables
c.execute("""DROP TABLE 'table_1'""")
c.execute("""DROP TABLE 'table_2'""")

# close connexion
conn.commit()
conn.close()


class TestDatabaseHandling(unittest.TestCase):

    def test_create_table_in_db(self):
        self.assertEqual(test_table_1_exist, ('table_1',))
        self.assertEqual(test_table_2_exist, ('table_2',))

    def test_insert_in_db_table(self):
        self.assertEqual(test_inserted_values_1, (1, 1, 'text'))
        self.assertEqual(test_inserted_values_2, (1, 'text'))

    def test_delete_from_db_table(self):
        self.assertIsNone(test_delete_values_1)

    def test_get_db_table_infos(self):
        self.assertEqual(d_table_2_infos['nrows'], 1)
        self.assertEqual(d_table_2_infos['columns'], ['var_1', 'var_2'])

    def test_db_table_to_dataframe(self):
        self.assertEqual(df_table_2[0].shape, (1, 2))
