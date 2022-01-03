from question_class import Question
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# For tests
data = {
    'ID_question': [1, 2, 3],
    'ID_theme': [1, 1, 2],
    'enonce': ['Q1', 'Q2', 'Q3'],
    'lien': ["L1", "L2", "L3"],
    'boite': [1, 2, 3]
}
df_test_data = pd.DataFrame.from_dict(data)

data_theme = {
    'ID_theme': [1, 2],
    'theme': ["theme1", "theme2"]
}
df_test_boite = pd.DataFrame.from_dict(data_theme)


def test_questions():
    # For test
    l_ = []
    for i in range(10000):
        q = Question(df_test_data, df_test_boite, "Question 1")
        l_.append(q.ID)

    print(l_.count(1) / 10000)
    print(l_.count(2) / 10000)
    print(l_.count(3) / 10000)


# test_questions()
conn = sqlite3.connect('../data/questions.db')
c = conn.cursor()

today_date = datetime.today()
yesterday_date = today_date - timedelta(days=1)

today_date_str = today_date.strftime('%Y-%m-%d')
yesterday_date_str = yesterday_date.strftime('%Y-%m-%d')

c.execute("DROP TABLE job_done_dates")
c.execute("""CREATE TABLE job_done_dates (date text)""")
c.execute("INSERT INTO job_done_dates VALUES ('" + today_date_str + "')")
c.execute("SELECT max(date) from job_done_dates")
conn.commit()
res = c.fetchall()

max_date = datetime.strptime(res[0][0], '%Y-%m-%d')
print(type(max_date))
print(type(yesterday_date))
print(type(today_date))
print("Max date: {}".format(max_date))
print("Yesterday date: {}".format(yesterday_date))
print("Today date: {}".format(today_date))
print("Max date < today: {}".format(max_date < today_date))
print("Max date = today: {}".format(max_date == today_date))
print("Max date > yesterday: {}".format(max_date > yesterday_date))
print("Max date = yesterday: {}".format(max_date == yesterday_date))

conn.close()
