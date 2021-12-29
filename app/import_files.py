import pandas as pd
import os
import sqlite3

# current path
path = os.path.dirname(__file__)
fichier_boite = path + '\..\data\Boites.csv'
fichier_questions = path + '\..\data\Questions.xlsx'

# fichier contenant les questions
# df_boite = pd.read_csv(fichier_boite)

# fichier contenant les boites des questions
df_questions = pd.read_excel(fichier_questions)

conn = sqlite3.connect('../data/questions.db')
c = conn.cursor()

df_db_questions = pd.read_sql_query("SELECT * FROM questions", conn)
df_db_themes = pd.read_sql_query("SELECT * FROM themes", conn)


