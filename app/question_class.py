import random


class Question:
    def __init__(self, df, df_theme, name=None):
        self.name = name
        # Pick a random question from the theme
        self.theme, self.ID, self.enonce, self.lien = pick_random_question(df, df_theme)


def pick_random_question(df, df_theme):
    # pick random theme
    theme_id = pick_random_theme(df_theme)
    theme = df_theme.loc[df_theme["ID_theme"] == theme_id, 'theme'].values[0]
    # get questions ids for theme
    df_theme = filter_dataframe(df, 'ID_theme', theme_id)
    l_q_id = df_theme["ID_question"].to_list()
    # compute weights with boite number
    l_q_weight = [1 / boite for boite in df_theme["boite"].to_list()]
    # get random id for theme according to weights
    random_id = random.choices(l_q_id, weights=l_q_weight)
    # get ID, enonce and lien
    Q_ID = random_id[0]
    enonce = df.loc[df["ID_question"] == Q_ID, 'enonce'].values[0]
    lien = df.loc[df["ID_question"] == Q_ID, 'lien'].values[0]

    return theme, Q_ID, enonce, lien


############################

def pick_random_theme(df_theme):
    l_theme_ids = list(set(df_theme['ID_theme']))
    random_theme_id = random.choice(l_theme_ids)
    return random_theme_id


def filter_dataframe(df, column, value):
    if type(value) == list and len(value) > 1:
        df_filtered = df.loc[df[column].isin(value)].copy()
    elif type(value) == list and len(value) == 1:
        df_filtered = df.loc[df[column] == value[0]].copy()
    else:
        df_filtered = df.loc[df[column] == value].copy()

    return df_filtered
