"""This module provides a class "Question" which is the heart of our learning system.

### Question class:
(see class docstring)

### Other functions
This modules also contains functions that help building these methods:
pick_random_question:
    pick a random question from a dataframe according to a topic
pick_random_topic:
    pick a random topic from a question
filter_dataframe:
    filter dataframe according to a column value/list of values
forward_box:
    update box level to next one (maximum 4)
backward_box:
    update box level to previous one (min 1
"""
import random


class Question:
    """
    Class question is the heart of our interval learning model.
    Questions objects are created by randomly picking it up from 2 dataframes:
    - one containing the different subjects,
    - one containing the questions.

    Questions come with different attributes:
    ID: int
        database unique ID for the question
    topic: string
        subject of the question (statistics, technology, ...)
    label: string
        the question text
    link: strng
        link to the answer of the question
    box:
        In flashcard learning, Leitner system is a simple implementation of
        the principle of spaced repetition, where cards are reviewed at
        increasing intervals.
        In Question class, boxes are used to compute random weights for the questions (weight=1/box),
        the higher the box, the lowest probability to pick it up.

    and methods:
    __init__:
        pick a random question in the database
    update_boxe:
        according to the answer of the question, box goes to next or previous
        level (min 1 - max 4)
    save_box_in_database:
        save boxe level in questions database

    """

    def __init__(self, df_question, df_topic, name=None):
        """Question constructor

        Questions objects are created by random selection.
        First, a topic is chosen, then a question of this topic

        Parameters
        ----------
        df_question: DataFrame
            DataFrame contianing questions
            ['ID_question', 'ID_topic', 'label', 'link', 'box']
        df_topic: DataFrame
            DataFrame containing topic
            ['ID_topic', 'topic']

        name: str
            question name (default=None)
        """
        self.name = name
        # pick a random topic
        topic_id, self.topic = pick_random_topic(df_topic)
        # Pick a random question and store attributes
        self.ID, self.label, self.link, self.box = pick_random_question(df_question, topic_id)

    def update_box(self, right_answer):
        """update question box whether the answer is right or false

        Parameters
        ----------
        right_answer: bool
            state whether the answer to the question is right or false

        """
        if right_answer:
            self.box = forward_box(self.box)
        else:
            self.box = backward_box(self.box)

    def save_box_in_database(self, conn):
        """save box attribute in question table of database

        Parameters
        ----------
        conn: sqlite3 connexion
            connexion to a question database

        """
        c = conn.cursor()
        c.execute("""UPDATE questions SET box={} WHERE ID_question= {}""".format(self.box, self.ID))


#############
#   Utils   #
#############

def pick_random_question(df_questions, topic_id):
    """Randomly pick a question for a given topic

    Random choice uses 1/box as weight

    Parameters
    ----------
    df_questions: DataFrame
        DataFrame containing questions
        columns = ['ID_question', 'ID_topic', 'label', 'link', 'box']
    topic_id: int
        chosen topic ID

    Returns
    -------
    int: question id
    string: question label
    string: questions link
    int: question box level
    """
    # get question ids for given topic
    df_topic = filter_dataframe(df_questions, 'ID_topic', topic_id)
    l_q_id = df_topic["ID_question"].to_list()
    # pick a random question using weights (w=1/box)
    l_q_weight = [1 / box for box in df_topic["box"].to_list()]
    random_id = random.choices(l_q_id, weights=l_q_weight)
    question_id = random_id[0]
    question_row = df_questions.loc[df_questions["ID_question"] == question_id]
    # get question attributes
    label = question_row['label'].values[0]
    link = question_row['link'].values[0]
    box = question_row['box'].values[0]

    return question_id, label, link, box


def pick_random_topic(df_topic):
    """Pick a random topic in topic dataframe

    Parameters
    ----------
    df_topic: DataFrame
        DataFrame containing topics ID and labels
        columns=['ID_topic', 'topic']

    Returns
    -------
    int:
        random topic ID
    """
    l_topic_ids = list(set(df_topic['ID_topic']))
    random_topic_id = random.choice(l_topic_ids)
    topic_name = df_topic.loc[df_topic["ID_topic"] == random_topic_id, 'topic'].values[0]

    return random_topic_id, topic_name


def filter_dataframe(df, column, value):
    """Filter DataFrame for a column and a value or a list of value

    Parameters
    ----------
    df: DataFrame
        DataFrame to filter
    column: str
        column name
    value: list or 1dim value
        values

    Returns
    -------
    DataFrame: filtered DataFrame
    """
    if type(value) == list:
        if len(value) > 1:
            df_filtered = df.loc[df[column].isin(value)].copy()
        else:
            df_filtered = df.loc[df[column] == value[0]].copy()
    else:
        df_filtered = df.loc[df[column] == value].copy()

    return df_filtered


def forward_box(box):
    """Increase box level (max 4)

    Parameters
    ----------
    box: int
        question box level

    Returns
    -------
    int: updated box
    """
    if box < 4:
        box += 1

    return box


def backward_box(box):
    """decrease box level (min 1)

    Parameters
    ----------
    box: int
        question box level

    Returns
    -------
    int: updated box
    """
    if box > 1:
        box -= 1

    return box
