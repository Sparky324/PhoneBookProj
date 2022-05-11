"""Эта библиотека содержит все функции приложения"""

import sqlite3 as sql
import prettytable as pt
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from secrets import token_hex

global id_f

def lexer(c):  
    """
        Эта функция делит вводимую строку на команду и аргумент
    """    
    lex = ''
    arg = ''
    l = True
    for i in c:
        if i == ' ' and l:
            l = False 
        elif l:
            lex += i
        else:
            arg += i
    return shell(lex,arg)


def shell(lex, arg):
    """
        Эта функция обрабатывает аргументы и запускает соответствующую функцию
    """
    if lex == 'exit':
        return True
    elif lex == 'show':
        print(show())
    elif lex == 'help':
        print(helper())
    elif lex == 'delete':
        print(delete_num(arg))
    elif lex == 'found':
        print(found(arg))
    elif lex == 'exporttxt':
        print(export_txt(arg))
    elif lex == 'token':
        print(generate_show_token(arg))
    elif lex == 'cloud':
        print(to_cloud())
    elif lex == 'exportxlsx':
        print(export_xlsx(arg))
    elif lex == 'import':
        print(import_file(arg))
    elif lex == 'add':
        print(add_num(arg))


def show():
    """
        Эта функция возвращает объект класса PrettyTable и отвечает
        за вывод базы данных на экран
    """
    x = pt.PrettyTable()
    x.field_names = ["Номер телефона", "Имя", "e-mail"]
    conn, cur = create_table()
    check_data = cur.execute("SELECT * FROM phone_book ORDER BY name ASC")
    all_res = check_data.fetchall()
    x.add_rows(data)
    return x

def add_num(x):
    """
        Эта функция получает на вход строку х, в которой находятся
        номер телефона, имя и почта пользователя, разделенные пробелом.
        Отвечает за добавление контакта в БД
    """
    try:
        conn, cur = create_table()

        number = tuple(x.split())

        cur.execute("SELECT * FROM phone_book WHERE phone_number = (?)", (number[0],))
        data = cur.fetchall()

        if len(data) != 0:
            return "Номер телефона уже занят"
        cur.execute("INSERT INTO phone_book VALUES(?, ?, ?);", number)
        conn.commit()
        return "Успешно добавлено"
    except IndexError:
        return "Команда введена некорректно"
    except sql.ProgrammingError:
        return "Команда введена некорректно"

def delete_num(x):
    """
        Эта функция получает на фход строку х - номер телефона.
        Удаляет контакт с данным номером
    """
    try:
        conn = sql.connect("C://PhoneBook/phone_book.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM phone_book WHERE phone_number = (?)", (x,))
        conn.commit()
        return "Успешно удалено"
    except sql.OperationalError:
        create_table()
        delete_num(x)

def helper():
    """
        Эта функция выводит на экран руководство по внутренним командам
    """
    return ("""=================================================================================================
Список команд и правила их написания:
    add <номер телефона> <имя> <электронная почта> - добавить новый контакт
    exit - закончить работу в приложении
    help - показать этот список
    delete <номер контакта> - удалить контакт
    show - показать список контактов
    exporttxt <путь к файлу> - произвести экспорт книги в файл .txt, аргумент path -  optional, default = "C://PhoneBook/"
    exportxlsx <путь к файлу> - произвести экспорт книги в файл .xlsx, аргумент path - optional, default = "C://PhoneBook/"
    found <тип поиска(имя - name, номер - number или почта - mail)> <переменная для поиска> - найти контакты по заданному критерию
    cloud - загрузить данные на Google Диск (потребуется авторизация черезе сервисы Google)
    import <путь к файлу> - импортировать данные из стороннего .xlsx файла
=================================================================================================
             """)

def export_txt(path):
    """
        Эта функция получает на вход строку - путь к папке.
        Создает файл .txt в указанной папке (при возможности) и экспортирует туда БД
    """
    if len(path) != 0:
        try:
            f = open(path + "phone_book.txt", 'w')
            f.write(show().get_string())
            f.close()
            return f"Файл успешно создан в {path}"
        except PermissionError:
            return "Путь недоступен. Попробуйте другой"
    path = "C://PhoneBook/"
    f = open(path + "phone_book.txt", 'w')
    f.write(show().get_string())
    f.close()
    return f"Файл успешно создан в {path}"

def export_xlsx(path):
    """
        Эта функция получает на вход строку - путь к папке.
        Создает файл .xlsx в указанной папке (при возможности) и экспортирует туда БД
    """
    conn, cur = create_table()
    check_data = cur.execute("SELECT * FROM phone_book")
    all_res = check_data.fetchall()
    data = pd.DataFrame(all_res)

    if len(path) != 0:
        try:
            data.to_excel(path + "phone_book.xlsx", header = ["Номер телефона", "Имя", "e-mail"])
            return f"Файл успешно создан в {path}"
        except PermissionError:
            return "Путь недоступен. Попробуйте другой"
    path = "C://PhoneBook/"
    data.to_excel(path + "phone_book.xlsx", header = ["Номер телефона", "Имя", "e-mail"])
    return f"Файл успешно создан в {path}"

def create_table():
    """
        Эта функция создает в БД таблицу (при отсутствии)
    """
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS phone_book(
                    phone_number TEXT,
                    name TEXT,
                    email TEXT);
                    """)
    conn.commit()
    return conn, cur

def found(x):
    """
        Эта функция получает на вход строку - тип поиска и строку для поиска через пробел.
        Вызывает одну из функций поиска в зависимости от типа
    """
    zapros = x.split()
    if zapros[0] == 'name':
        return found_name(zapros[1])
    elif zapros[0] == 'number':
        return found_num(zapros[1])
    elif zapros[0] == 'mail':
        return found_mail(zapros[1])
    else:
        return "Ошибка: неправильный аргумент типа"

def found_name(x):
    """
        Эта функция получает на вход строку - имя искомого контакта
        Возвращает объект класса PrettyTable с контактами, подходящими по данному критерию
    """
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM phone_book WHERE name = (?)", (x,))
    data = cur.fetchall()

    y = pt.PrettyTable()
    y.field_names = ["Номер телефона", "Имя", "e-mail"]

    for i in data:
        y.add_row(i)

    return y

def found_num(x):
    """
        Эта функция получает на вход строку - номер телефона искомого контакта
        Возвращает объект класса PrettyTable с контактами, подходящими по данному критерию
    """
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM phone_book WHERE phone_number = (?)", (x,))
    data = cur.fetchall()

    y = pt.PrettyTable()
    y.field_names = ["Номер телефона", "Имя", "e-mail"]

    y.add_rows(data)

    return y

def found_mail(x):
    """
        Эта функция получает на вход строку - e-mail искомого контакта
        Возвращает объект класса PrettyTable с контактами, подходящими по данному критерию
    """
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM phone_book WHERE email = (?)", (x,))
    data = cur.fetchall()

    y = pt.PrettyTable()
    y.field_names = ["Номер телефона", "Имя", "e-mail"]

    y.add_rows(data)

    return y

def to_cloud():
    """
        Эта функция получает отвечает за авторизаци пользователя в аккаунте Google 
        для последующего экспорта данных на его Google Drive
    """
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    global id_f

    try:
        file = drive.CreateFile({'id': id_f})
        file.Delete()
    except Exception as ex:
        print('')

    up_file = drive.CreateFile({'title': "phone_book.xlsx"})
    export_xlsx('')
    up_file.SetContentFile("C://PhoneBook/phone_book.xlsx")
    up_file.Upload()
    id_f = up_file['id']
    return "Файл успешно загружен на Ваш Google Диск."

def import_file(path):
    """
        Эта функция получает на вход строку - пуьть к файлу .xlsx
        Импортирует контакты из файла по заданному пути.
        ВНИМАНИЕ - предыдущие данные в БД будут стерты
    """
    conn, cur = create_table()

    cur.execute("DELETE FROM phone_book;")
    conn.commit()

    try:
        data = pd.read_excel(path)
        data.drop(data.columns[0], axis = 1, inplace = True)
        data = list(data.itertuples(index=False, name=None))

        cur.executemany("INSERT INTO phone_book VALUES(?, ?, ?)", (data))
        conn.commit()
        return "Успешно импортировано"
    except FileNotFoundError:
        return "Файл по заданному пути не найден"
