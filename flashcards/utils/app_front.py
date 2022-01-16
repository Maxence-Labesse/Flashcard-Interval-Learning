""" This module provides functions to build the software interface

function
--------
open_app:
    open software interface
show_question:
    open question window if button is pressed
close_question:
    modify interface and database when a question is answered
"""
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import webbrowser
import sqlite3
from flashcards.parameters import questions_db_path
from flashcards.utils.database_handling import db_conn, insert_in_db_table

# parameters
today = datetime.today()
first_question_done = False


def open_app(q1, q2, today_job_done):
    """build app interface

    This windows contains the date of the current day,
    and 1 button to open each question

    If the questions have already been answered this day, the interface
    doesn't show any question

    Parameters
    ----------
    q1: Question
        question1
    q2: Question
        question2
    today_job_done: bool
        If true, interface shows 2 questions.
        Just notify job is done otherwise

    Returns
    -------
    root: tkinter.Tk
        built app
    """
    # Creating main window
    root = Tk()
    root.title("Daily questions")
    style = ttk.Style()
    style.theme_use('clam')

    # Root Default Structure
    date_label = Label(root, text=today.date(), width=35)
    date_label.grid(row=0, column=1, columnspan=3, padx=50, pady=10)

    # If questions answered for current day, just notify it
    if today_job_done:
        root.configure(background='red')
        done_label = ttk.Button(root, text="Job done for today", command=lambda: root.destroy())
        done_label.grid(row=1, column=1, columnspan=3, padx=50, pady=10)

    # else, show button for each question
    else:
        q1_button = ttk.Button(root, text="Question1", command=lambda: show_question(root, q1))
        q2_button = ttk.Button(root, text="Question2", command=lambda: show_question(root, q2))
        q1_button.grid(row=1, column=1, pady=10)
        q2_button.grid(row=1, column=3, pady=10)

    return root


def show_question(root, question):
    """Open question window when a question button is pressed

    This winwow presents:
    - The topic and the label of the question
    - 2 buttons to notify whether you know the answer or not
    - A button that links to the answer URL

    Parameters
    ----------
    root: tkinter.Tk
        inteface main window
    question: Question
        question to answer
    """
    # Open a new tkinter window
    global top
    top = Toplevel()
    top.title(question.name)

    # display question topic and label
    txt_topic = "Topic: {}".format(question.topic)
    txt_label = question.label
    width_label = max([len(x) for x in [txt_topic, txt_label]])
    topic_label = Label(top, text=txt_topic, anchor="w", width=width_label)
    topic_label.grid(row=0, column=0, columnspan=3, pady=10, padx=0)
    label_label = Label(top, text=txt_label, anchor="w", width=width_label)
    label_label.grid(row=1, column=0, columnspan=3, pady=10, padx=0)

    # link button (for answer web page)
    lien = ttk.Button(top, text="Link", command=lambda: webbrowser.open_new(url=question.link))
    lien.grid(row=3, column=2, pady=10, padx=20)

    # answers buttons (whether you know or don't know the answer
    right_answer_button = ttk.Button(top, text="I know",
                                     command=lambda: close_question(root, question, right_answer=True))
    right_answer_button.grid(row=2, column=1, pady=10, padx=20)
    false_answer_button = ttk.Button(top, text="I don't know",
                                     command=lambda: close_question(root, question, right_answer=False))
    false_answer_button.grid(row=2, column=3, pady=10, padx=20)


def close_question(root, question, right_answer):
    """modify interface and database when a question is answered

    1. update question box level according to answer, and save
       it in the database
       If true, box+=1 (max 4), else box-=1 (min 1)
    2. if both questions have been answered, save current day as
       done and close the app
       else, disable question button and close answer window


    Parameters
    ----------
    root: tkinter.Tk
        inteface main window
    question: Question
        question to answer
    right_answer: bool
        True or False answer to the question
    """
    top.destroy()
    global first_question_done
    question.update_box(right_answer)

    # update and save box level
    conn = sqlite3.connect(questions_db_path)
    question.save_box_in_database(conn)
    conn.close()

    # if both questions have been answered, save current day in database
    # and close app
    if first_question_done:
        today_str = today.date().strftime("%Y-%m-%d")
        messagebox.showinfo(title="Good job !", message="Job done for today !")
        db_conn(questions_db_path, insert_in_db_table, table_name="job_done_dates", list_values=[today_str])
        root.destroy()

    # else, disable answered question button
    else:

        if question.name == "Question 1":
            q1_button = ttk.Button(root, text="Question1", state=DISABLED,
                                   command=lambda: show_question(root, question))
            q1_button.grid(row=1, column=1, pady=10)
        else:
            q2_button = ttk.Button(root, text="Question2", state=DISABLED,
                                   command=lambda: show_question(root, question))
            q2_button.grid(row=1, column=3, pady=10)

        first_question_done = True

