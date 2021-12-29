import sqlite3
import pandas as pd
from app.import_files import df_questions, fichier_questions


def update_db(df):
    df_tmp = df.copy()

    # For each question in Questions file
    for index, row in df_tmp.iterrows():

        # If 'DB' column is not 'OK', add the question in database
        if row['Db'] != "OK":
            c.execute("SELECT ID_theme from themes where theme='{}'".format(row['Theme']))
            res = c.fetchone()

            # if theme is not in themes table, add it with a new id_theme
            if res is None:
                insert_in_db_table("themes", "(NULL, '{}')".format(row['Theme']))
                c.execute("SELECT ID_theme from themes where theme='{}'".format(row['Theme']))
                res = c.fetchone()
                print("'{}' new theme has been added with id_theme {}".format(row['Theme'], res[0]))
            # Now theme exists in themes table, add question in questions table, and set boite to 1
            theme_id = res[0]

            insert_in_db_table("questions",
                               '(NULL, "{}", "{}", "{}", "{}")'.format(theme_id, row['Enonce'], row["Lien"], 1))

            # set 'DB' as 'OK
            df_tmp.loc[index, 'Db'] = 'OK'

            print("row {} has been added".format(index))

    return df_tmp


def insert_in_db_table(table_name, values):
    """
    Inster many values:
    https://youtu.be/byHcYRpMgI4?t=1887
    """
    c.execute("INSERT INTO {} VALUES {}".format(table_name, values))
    conn.commit()


def db_table_to_dataframe(table_name, keep_rowid=False):
    if keep_rowid:
        df = pd.read_sql_query("SELECT rowid, * from {}".format(table_name), conn)
    else:
        df = pd.read_sql_query("SELECT * from {}".format(table_name), conn)
    return df


def delete_from_db_table(table_name, rowid):
    c.execute("DELETE from {} where rowid={}".format(table_name, str(rowid)))


def create_tables():
    c.execute("DROP TABLE questions")
    c.execute("DROP TABLE themes")

    c.execute("""CREATE TABLE themes (
            ID_theme INTEGER PRIMARY KEY AUTOINCREMENT,
            theme text
    )""")

    c.execute("""CREATE TABLE questions (
            ID_question INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_theme Integer,
            enonce text,
            lien text,
            boite Integer
    )""")


####################################################

conn = sqlite3.connect('../data/questions.db')
c = conn.cursor()

# create_tables()

df_filled = update_db(df_questions)

print(df_filled)
print(pd.read_sql_query("SELECT ID_theme, theme from themes", conn))
print(pd.read_sql_query("SELECT * from questions", conn))

df_filled.to_excel(fichier_questions, index=False)

conn.commit()

conn.close()
