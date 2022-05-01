import sqlite3 as sql
import os

def create_directory(path):
    try:
        os.makedirs(path)
        return (f"Directory file succesfully created: {path}")
    except FileExistsError:
        return (f"Diretory {path} already exists")

def create_db(name, path):
    if os.path.isfile(path + "/" + name):
        return (f"Database already exists. Reading...")
    else:
        conn = sql.connect(path + "/" + name)
        return (f"Database succesfully created in {path}")