"""

"""
from utils import test_same_dates
import sqlite3
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from utils.questions import Question
from parameters import questions_db_path
from sqlite3_utils.db_handling import insert_in_db_table, db_conn, prepare_data_for_db_insert, \
    db_table_to_dataframe

import webbrowser

# import database tables (utils, themes and job_done_dates)
l_table_names = ['utils', 'themes', 'job_done_dates']
conn = sqlite3.connect(questions_db_path)
l_imported_df = db_table_to_dataframe(conn, l_table_names)
conn.close()
df_questions, df_themes, df_job_done_dates = l_imported_df[0], l_imported_df[1], l_imported_df[2]

# test if today's utils are already done
last_done_date = df_job_done_dates['date'].max()
today = datetime.today()
today_job_done = test_same_dates(last_done_date, today)

# pick 2 random utils
q1 = Question(df_questions, df_themes, "Question 1")
q2 = Question(df_questions, df_themes, "Question 2")


#########
# Front #
#########
# Global window settings
root = Tk()
root.title("2 Questions A Day")
if today_job_done: root.configure(background='red')
# root.iconbitmap("/images/icon2.ico")
style = ttk.Style()
style.theme_use('clam')

'''
def close_question(question, right_answer):
    top.destroy()
    global first_question_done
    global df_questions
    question.update_box(right_answer)
    
    conn = sqlite3.connect(questions_db_path)
    question.save_box_level_in_database(conn)
    conn.close

    if first_question_done:
        messagebox.showinfo(title="Good job !", message="Job done for today !")
        date_prepared = prepare_data_for_db_insert([today_date_str], primary_key=False)
        db_conn(questions_db_path, insert_in_db_table, table_name="job_done_dates", values=date_prepared)
        root.destroy()
    else:

        if question.name == "Question 1":
            q1_button = ttk.Button(root, text="Question1", state=DISABLED, command=lambda: open_question(q1))
            q1_button.grid(row=1, column=1, pady=10)
        else:
            q2_button = ttk.Button(root, text="Question2", state=DISABLED, command=lambda: open_question(q2))
            q2_button.grid(row=1, column=3, pady=10)

        first_question_done = True


def open_question(question):
    """
    when "Open Second Window" button is pressed, an image is displayed in a new window
    """
    # Opening a new window
    global top
    top = Toplevel()
    top.title(question.name)

    # Labels
    txt_theme = "Theme: {}".format(question.theme)
    txt_enonce = "Enoncé: {}".format(question.enonce)

    def callback():
        webbrowser.open_new(url=question.lien)

    width_label = max([len(x) for x in [txt_theme, txt_enonce]])

    theme_label = Label(top, text=txt_theme, anchor="w", width=width_label)
    theme_label.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

    enonce_label = Label(top, text=txt_enonce, anchor="w", width=width_label)
    enonce_label.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

    # lien_label = Label(top, text=txt_lien, anchor="w", width=width_label)
    # lien_label.grid(row=2, column=0, columnspan=3, pady=10, padx=20)
    # lien_label.bind("<Button-1>", lambda event: webbrowser.open(lien_label.cget("text")))

    lien = ttk.Button(top, text="Lien", command=callback)
    lien.grid(row=3, column=2, pady=10, padx=20)

    bonne_reponse_button = ttk.Button(top, text="Je sais", command=lambda: close_question(question, right_answer=True))
    bonne_reponse_button.grid(row=2, column=1, pady=10, padx=20)

    mauvaise_reponse_button = ttk.Button(top, text="Je ne sais pas",
                                         command=lambda: close_question(question, right_answer=False))
    mauvaise_reponse_button.grid(row=2, column=3, pady=10, padx=20)


# Root Default Structure
date_label = Label(root, text=today_date_str, width=35)
date_label.grid(row=0, column=1, columnspan=3, padx=50, pady=10)

if today_done:
    done_label = ttk.Button(root, text="Job done for today", command=lambda: root.destroy())
    done_label.grid(row=1, column=1, columnspan=3, padx=50, pady=10)

else:
    q1_button = ttk.Button(root, text="Question1", command=lambda: open_question(q1))
    q2_button = ttk.Button(root, text="Question2", command=lambda: open_question(q2))
    q1_button.grid(row=1, column=1, pady=10)
    q2_button.grid(row=1, column=3, pady=10)

# Loop for dynamic screen
root.mainloop()
'''
