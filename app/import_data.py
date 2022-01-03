import pandas as pd
import os
import sqlite3

# paths
dir_path = os.path.dirname(__file__)
questions_file_path = dir_path + '\..\data\Questions.xlsx'
questions_db_path = dir_path + '\..\data\questions.db'

# fichier contenant les boites des questions
df_questions = pd.read_excel(questions_file_path)

conn = sqlite3.connect(questions_db_path)
c = conn.cursor()
df_db_questions = pd.read_sql_query("SELECT * FROM questions", conn)
df_db_themes = pd.read_sql_query("SELECT * FROM themes", conn)
c.execute("SELECT max(date) from job_done_dates")
last_done_date_str = c.fetchall()[0][0]
conn.commit()
conn.close()
