import sqlite3
import pandas as pd


def db_conn(db_path, func, *args, **kwargs):
    """
    Open and close a connexion to a database to directly execute a SQL request function
    """
    # Open connexion
    conn = sqlite3.connect(db_path)
    # Create cursor
    c = conn.cursor()
    func(c, *args, **kwargs)
    # commit sql request function
    conn.commit()
    # Close connexion
    conn.close()


#########################
# SQL Request functions #
#########################

def create_table_in_db(c, table_name, d_var_types, drop=False):
    """
    Creates a table in a database

    If drop=True, drop the table first
    """
    if drop:
        try:
            c.execute("""DROP TABLE {}""".format(table_name))
        except sqlite3.OperationalError:
            print("Table can't be dropped because does not exist")

    c.execute("""CREATE TABLE {} ({})""".format(table_name,
                                                concat_list(concat_key_value(d_var_types), ',')
                                                ))


def insert_in_db_table(c, table_name, values):
    """
    Insert a new row into a db
    """
    c.execute("INSERT INTO {} VALUES {}".format(table_name, values))


def delete_from_db_table(c, table_name, rowid):
    c.execute("DELETE from {} where rowid={}".format(table_name, str(rowid)))


def display_db_table(conn, table_name):
    print(pd.read_sql_query("SELECT * from {}".format(table_name), conn))


#############################
# Data processing functions #
#############################
def prepare_data_for_db_insert(data_list, primary_key=False):
    """
    Prepare data to be insert in a database (val1, ..., valn)

    if primary_key=True, add Null value as first element
    """
    if primary_key:
        return "(NULL, " + concat_list(data_list, ",", quote_str=True) + ")"
    else:
        return "(" + concat_list(data_list, ",", quote_str=True) + ")"


def concat_list(str_list, sep, quote_str=False):
    """
    Concat elements of a list into a string with a separator,

    if quote_str is True, quote strings elements
    """
    # First element from the list
    first_element = to_str(str_list[0], quote_str)
    concat_str = first_element

    # If there are more than 1 element in the list, concat elements
    if len(str_list) > 0:
        for i in range(1, len(str_list)):
            new_element = to_str(str_list[i], quote_str)
            concat_str = concat_str + sep + new_element
    return concat_str


def to_str(val, add_quote=False):
    """
    test if a value's type is string. It not, transform it to string

    If add_quote=True, add quotes to string
    """
    if is_str(val) and add_quote:
        return "\'" + val + "\'"
    elif is_str(val):
        return val
    else:
        return str(val)


def is_str(txt):
    """
    Test if a value's type is string
    """
    return type(txt) == str


def concat_key_value(str_dict):
    """
    concat keys and values of dict containing strings elements into a list
    {key1: value1, key2: value2} --> ['key1 value1', 'key2 value2']
    """
    return [key + ' ' + value for key, value in str_dict.items()]
