#""" ������ ��� �������� �����/���������� """

import sqlite3 as sql
from time import sleep
import os

def create_directory(path):
    #sleep(2)
    try:
        os.makedirs(path)
        return (f"Directory file succesfully created: {path}")
    except FileExistsError:
        return (f"Diretory {path} already exists")

def create_db(name, path):
    #sleep(2)
    if os.path.isfile(path + "/" + name):
        return (f"Database already exists. Reading...")
    else:
        conn = sql.connect(path + "/" + name)
        return (f"Database succesfully created in {path}")