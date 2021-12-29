from question_class import Question
import pandas as pd

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


test_questions()
