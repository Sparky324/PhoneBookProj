import sqlite3 as sql
import os

def create_directory(path):
    try:
        os.makedirs(path)
        return (f"Директория создана: {path}")
    except FileExistsError:
        return (f"Директория {path} уже существует")

def create_db(name, path):
    if os.path.isfile(path + "/" + name):
        return (f"Файл базы данных уже существует. Чтение...")
    else:
        conn = sql.connect(path + "/" + name)
        return (f"Файл базы данных успешно создан в {path}")