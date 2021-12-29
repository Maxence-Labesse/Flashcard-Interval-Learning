"""

"""
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from question_class import Question
from import_files import df_db_questions, df_db_themes
from boites import avancer_boite, reculer_boite, save_boite
import webbrowser

# Initial Parameters
today_date = datetime.today().strftime('%Y-%m-%d')
today_done = False
first_question_done = False

# pick 2 random questions
q1 = Question(df_db_questions, df_db_themes, "Question 1")
q2 = Question(df_db_questions, df_db_themes, "Question 2")

# Global window settings
root = Tk()
root.title("2 Questions A Day")
if today_done: root.configure(background='red')
# root.iconbitmap("/images/icon2.ico")
style = ttk.Style()
style.theme_use('clam')


def close_question(question, bonne_reponse):
    top.destroy()
    global first_question_done
    global df_boite

    if bonne_reponse:
        df_boite = avancer_boite(df_boite, question.ID)
    else:
        df_boite = reculer_boite(df_boite, question.ID)

    if first_question_done:
        messagebox.showinfo(title="Good job !", message="Job done for today !")
        save_boite(df_boite)
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

    bonne_reponse_button = ttk.Button(top, text="Je sais", command=lambda: close_question(question, bonne_reponse=True))
    bonne_reponse_button.grid(row=2, column=1, pady=10, padx=20)

    mauvaise_reponse_button = ttk.Button(top, text="Je ne sais pas",
                                         command=lambda: close_question(question, bonne_reponse=False))
    mauvaise_reponse_button.grid(row=2, column=3, pady=10, padx=20)


# Root Default Structure
date_label = Label(root, text=today_date, width=35)
date_label.grid(row=0, column=1, columnspan=3, padx=50, pady=10)

if today_done:
    done_label = ttk.Button(root, text="Job done for today")
    done_label.grid(row=1, column=1, columnspan=3, padx=50, pady=10)

else:
    q1_button = ttk.Button(root, text="Question1", command=lambda: open_question(q1))
    q2_button = ttk.Button(root, text="Question2", command=lambda: open_question(q2))
    q1_button.grid(row=1, column=1, pady=10)
    q2_button.grid(row=1, column=3, pady=10)

# Loop for dynamic screen
root.mainloop()
