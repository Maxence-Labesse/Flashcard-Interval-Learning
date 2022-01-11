"""This module provides function related to database handling (sqlite3
    requests)

db_conn
    encapsulate a SQL requests function with opening and closing
    database connexion
create_table_in_db
    create a table in a database
insert_in_db_table
    insert values in a database table
delete_from_db_table
    delete row from database table
get_db_table_infos
    display database table infos (nrows and column names)
db_table_to_dataframe
    import database table in a DataFrame

This module uses string_processing module for data formatting
"""
import sqlite3
import pandas as pd
from flashcards.utils.string_processing import *


def db_conn(db_path, func, *args, **kwargs):
    """Encapsulates a function with database connexion

    - open connexion to a database
    - execute the function
    - commit and close connexion

    first function argument has to be a sqlite3 connexion,
    then use db_conn as follow:
    for func(conn, arg2, arg3), db_conn(db_path, func, arg2, arg3)

    Parameters
    ----------
    db_path: string
        path to database
    func: func
        function to encapsulate
    """
    # Open connexion and create cursor
    conn = sqlite3.connect(db_path)

    func(conn, *args, **kwargs)
    # close connexion
    conn.commit()
    conn.close()


#########################
# SQL Request functions #
#########################

def create_table_in_db(conn, table_name, d_var_types, drop=False):
    """create a table in a database

    If drop=True, drop the table first

    Parameters
    ----------
    conn: sqlite3 Connexion
        connexion to a sqlite3 database
    table_name: str
        name of the table to create
    d_var_types:
        dict containing variables names and their type
        (values are all strings)
        {"var_1": "type_1", ..., "var_n", "type_n"]
    drop: bool
        if True, try to drop the table first
    """
    c = conn.cursor()
    if drop:
        try:
            c.execute("""DROP TABLE {}""".format(table_name))
        except sqlite3.OperationalError:
            print("Table can't be dropped because does not exist")

    c.execute("""CREATE TABLE {} ({})""".format(table_name,
                                                concat_list(concat_key_value(d_var_types), ',')
                                                ))


def insert_in_db_table(conn, table_name, list_values, primary_key=False):
    """insert a new row in a datable

    Parameters
    ----------
    conn: sqlite3 Connexion
        connexion to a sqlite3 database
    table_name: str
        table name
    values: list
        values to include in the row
        [val_1, ..., val_n]
    primary_key: bool
        True if the table contains a primary key as first column
    """
    row_to_insert = prepare_data_for_db_insert(list_values, primary_key=primary_key)
    c = conn.cursor()
    c.execute("INSERT INTO {} VALUES {}".format(table_name, row_to_insert))


def delete_from_db_table(conn, table_name, rowid):
    """Using a Delete a row for a given rowid

    Parameters
    ----------
    conn: sqlite3 Connexion
        connexion to a sqlite3 database
    table_name: str
        table name
    rowid: int
        rowid of the row to delete
    """
    c = conn.cursor()
    c.execute("DELETE from {} where rowid={}".format(table_name, str(rowid)))


def get_db_table_infos(conn, table_name):
    """get row_number and columns table of a database table

    Parameters
    ----------
    conn: sqlite3 Connexion
        connexion to a sqlite3 database
    table_name: str
        table name

    Returns
    -------
    dict:
        dictionnary containing table row numbers and columns
        {"nrows": val, "columns": val
    """
    df = pd.read_sql_query("SELECT * from {}".format(table_name), conn)

    return {"nrows": df.shape[0], "columns": df.columns.tolist()}


def db_table_to_dataframe(conn, l_table_names):
    """import databse tables into dataframes

    Parameters
    ----------
    conn: sqlite3 Connexion
        connexion to a sqlite3 database
    l_table_names: list
        list containing names of the tables to import

    Returns
    -------
    list:
        list containing dataframes

    """
    df_list = []

    for table_name in l_table_names:
        df = pd.read_sql_query("SELECT * FROM {}".format(table_name), conn)
        df_list.append(df)

    return df_list
