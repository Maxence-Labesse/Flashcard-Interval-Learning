from flashcards.utils.database_handling import *

d_var_types_questions = {
    'ID_question': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'ID_topic': 'int',
    'label': 'text',
    'link': 'text',
    'box': 'int'
}

d_var_types_themes = {
    'ID_topic': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'topic': 'text'
}


def update_db(c, df):
    df_tmp = df.copy()

    # For each question in Questions file
    for index, row in df_tmp.iterrows():

        # If 'DB' column is not 'OK', add the question in database
        if row['Db'] != "OK":
            c.execute("SELECT ID_theme from themes where theme='{}'".format(row['Theme']))
            res = c.fetchone()

            # if theme is not in themes table, add it with a new id_theme
            if res is None:
                theme_values = [row['Theme']]
                theme_values_prepared = prepare_data_for_db_insert(theme_values, primary_key=True)
                insert_in_db_table(c, "themes", theme_values_prepared)

                # get new id_theme to add id to utils table
                c.execute("SELECT ID_theme from themes where theme='{}'".format(row['Theme']))
                res = c.fetchone()
                print("'{}' new theme has been added with id_theme {}".format(row['Theme'], res[0]))

            # Now theme exists in themes table, add question in utils table, and set boite to 1
            theme_id = res[0]
            question_values = [theme_id, row['Enonce'], row["Lien"], 1]
            question_values_prepared = prepare_data_for_db_insert(question_values, primary_key=True)
            insert_in_db_table(c, "utils", question_values_prepared)

            # set 'DB' as 'OK
            df_tmp.loc[index, 'Db'] = 'OK'

            print("row {} has been added".format(index))

    return df_tmp


conn = sqlite3.connect(questions_db_path)
c = conn.cursor()
create_table_in_db(c, "themes", d_var_types_themes, drop=True)
create_table_in_db(c, "utils", d_var_types_questions, drop=True)
update_db(c, df_questions)
display_db_table(conn, "themes")
display_db_table(conn, "utils")
display_db_table(conn, "job_done_dates")
conn.commit()
conn.close()
