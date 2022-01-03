from import_data import dir_path
import sqlite3


def avancer_boite(boite):
    if boite < 4:
        boite += 1

    return boite


def reculer_boite(boite):
    if boite > 0:
        boite -= 1

    return boite


def update_boite(id_question, boite):
    conn = sqlite3.connect(dir_path + '\..\data\questions.db')
    c = conn.cursor()
    c.execute("""UPDATE questions SET boite={} WHERE ID_question= {}""".format(boite, id_question))
    conn.commit()
    conn.close()
