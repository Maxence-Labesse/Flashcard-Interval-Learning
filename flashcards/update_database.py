""" This module/script purpose is to update questions database from
    an Excel file.

The question database contains 2 tables:
- questions(columns: ID_question, ID_topic, label, link, box)
- topics (columns: ID_topic, topic)

The Excel file purpose is to add new questions to the database
Excel columns are: Imported, Topic, Label, Link


functions
---------
add_questions:
    add new questions from the Excel file to the database
create_database:
    create database if it's the first time you use this software

commmand line
-------------
these functions are executed with command line
- To add new questions to database
  In terminal (in root folder):
  python -m flashcards.update_database update data/Questions.xlsx

- To create database (or reset it with empty tables)
  In terminal (in root folder):
  python -m flashcards.update_database create

"""
import argparse
from flashcards.utils.database_handling import *
from flashcards.parameters import questions_db_path, update_questions_file_path


def add_questions(conn, args):
    """add new question from the Excel file to the database

    For a question in the Excel file, if the 'Imported' column is not "OK",
    add the question in questions table of the database. If the topic of
    the questions does not exist in topic table, add it.

    The 'Imported' column of Excel file is then filled and Excel file
    is updated

    Parameters
    ----------
    ----------
    conn: sqlite3 Connexion
        connexion to a sqlite3 database
    update_file_path:
        path to the Excel update file
    """
    c = conn.cursor()
    df_tmp = pd.read_excel(args.QuestionExcelfile).copy()

    ct_new_questions = 0
    ct_new_topics = 0
    # for each question in Questions file
    for index, question in df_tmp.iterrows():

        # if the question has not been imported yet, add the question in database
        if question['Imported'] != "OK":

            # if question topic does not exist in topics table, else get its ID
            c.execute("SELECT ID_topic from topics where topic='{}'".format(question['Topic']))
            res = c.fetchone()
            if res is None:
                # create new topic in topics table and get its ID_topic
                insert_in_db_table(conn, "topics", [question['Topic']], primary_key=True)
                c.execute("SELECT ID_topic from topics where topic='{}'".format(question['Topic']))
                topic_id = c.fetchone()[0]
                ct_new_topics += 1
            else:
                topic_id = res[0]

            # now topic exists in topics table, add question in utils table,
            # and set box to 1 (start level)
            question_values = [topic_id, question['Label'], question["Link"], 1]
            insert_in_db_table(conn, "questions", question_values, primary_key=True)

            # set 'Imported' as 'OK'
            df_tmp.loc[index, 'Imported'] = 'OK'
            ct_new_questions += 1

    print("{} topics have been added".format(ct_new_topics))
    print("{} questions have been added".format(ct_new_questions))
    df_tmp.to_excel(args.QuestionExcelfile, index=False)


def create_database(conn, args):
    """Create question database tables

    Parameters
    ----------
    conn: sqlite3 Connexion
        connexion to a sqlite3 database

    Returns
    -------

    """
    d_var_types_questions = {
        'ID_question': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'ID_topic': 'int',
        'label': 'text',
        'link': 'text',
        'box': 'int'
    }

    d_var_types_topics = {
        'ID_topic': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'topic': 'text'
    }

    d_var_job_done_dates = {
        'date': 'text'
    }

    # Empty Imported column in update Excel file
    create_table_in_db(conn, "topics", d_var_types_topics, drop=True)
    create_table_in_db(conn, "questions", d_var_types_questions, drop=True)
    create_table_in_db(conn, 'job_done_dates', d_var_job_done_dates, drop=True)

    print("table have been created")


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

update_parser = subparsers.add_parser('update')
update_parser.add_argument('QuestionExcelfile', help='path to your .xslx file')
update_parser.set_defaults(func=add_questions)

create_parser = subparsers.add_parser('create')
create_parser.set_defaults(func=create_database)

reset_parser = subparsers.add_parser('reset')
reset_parser.set_defaults(func=create_database)

if __name__ == "__main__":
    con = sqlite3.connect(questions_db_path)
    args = parser.parse_args()
    args.func(con, args)  # call the default function
    con.commit()
    con.close()
