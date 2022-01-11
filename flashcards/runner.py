"""This is the main script of the flashcard learning software

"""
from flashcards.utils.date_utils import test_same_dates
import sqlite3
from datetime import datetime
from flashcards.utils.questions import Question
from flashcards.parameters import questions_db_path
from flashcards.utils.database_handling import db_table_to_dataframe
from flashcards.utils.app_front import open_app


def main():
    # import database tables into dataframes
    l_table_names = ['questions', 'topics', 'job_done_dates']
    conn = sqlite3.connect(questions_db_path)
    l_imported_df = db_table_to_dataframe(conn, l_table_names)
    conn.close()
    df_questions, df_topics, df_job_done_dates = l_imported_df[0], l_imported_df[1], l_imported_df[2]

    # test if questions have already been answered for current
    # day
    last_done_date = df_job_done_dates['date'].max()
    if isinstance(last_done_date, str):
        today = datetime.today()
        today_job_done = test_same_dates(last_done_date, today)
    else:
        today_job_done = False

    # pick 2 random questions
    q1 = Question(df_questions, df_topics, "Question 1")
    q2 = Question(df_questions, df_topics, "Question 2")

    # open interface
    root = open_app(q1, q2, today_job_done)
    root.mainloop()


if __name__ == "__main__":
    main()
