"""This file contains paths to data

By default, data is in a folder at the root of the project (at the same level as flashcards folder)

questions_db_path:
    path to database that contains flashcard questions
update_questions_file_path:
    path to excel file used to update the database with new questions
"""
import os

# paths
root_path = os.path.dirname(__file__)
questions_db_path = root_path + '\..\data\questions.db'
update_questions_file_path = root_path + '\..\data\Questions.xlsx'

