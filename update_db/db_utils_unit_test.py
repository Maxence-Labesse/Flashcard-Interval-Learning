from handle_db_utils import *

##############
# Parameters #
##############
test_db = 'unit_tests_db.db'

d_var_types = {
    'ID': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'var1_int': 'int',
    'var2_txt': 'text'
}

value_1 = [1, 'text1']
value_2 = [1, 'text2']

###########
#   SQL   #
###########
# Create "tests" table according to d_var_types (drop it if it already exists)
db_conn(test_db, create_table_in_db, table_name="tests", d_var_types=d_var_types, drop=True)
print("\n")
# Prepare data to be inserted in table
print("-- Data Preparation --")
value_1_prepared = prepare_data_for_db_insert(value_1, primary_key=True)
value_2_prepared = prepare_data_for_db_insert(value_2, primary_key=True)
print(value_1_prepared)
print(value_2_prepared)
print("\n")

conn = sqlite3.connect(test_db)
display_db_table(conn, "tests")
conn.close()
print("\n")
db_conn(test_db, insert_in_db_table, table_name="tests", values=value_1_prepared)
conn = sqlite3.connect(test_db)
display_db_table(conn, "tests")
conn.close()
print("\n")
db_conn(test_db, insert_in_db_table, table_name="tests", values=value_2_prepared)
conn = sqlite3.connect(test_db)
display_db_table(conn, "tests")
conn.close()
