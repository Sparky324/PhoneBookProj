"""Эта библиотека отвечает за логику создания главных файлов приложения"""

import sqlite3 as sql
import os

def create_directory(path):
    """
        Эта функция создает директорию для файлов приложения
    """
    try:
        os.makedirs(path)
        return (f"Директория создана: {path}")
    except FileExistsError:
        return (f"Директория {path} уже существует")

def create_db(name, path):
    """
        Эта функция создает файл базы данных в директории
    """
    if os.path.isfile(path + "/" + name):
        return (f"Файл базы данных уже существует. Чтение...")
    else:
        conn = sql.connect(path + "/" + name)
        return (f"Файл базы данных успешно создан в {path}")