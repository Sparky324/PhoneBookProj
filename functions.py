import sqlite3 as sql
import prettytable as pt
import pandas as pd

def lexer(c):      
                   
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
    if lex == 'echo':
        print(arg)
    elif lex == 'exit':
        return True
    elif lex == 'show':
        print(show())
    elif lex == 'help':
        print(helper())
    elif lex == 'delete':
        delete_num(arg)
    elif lex == 'exporttxt':
        print(export_txt())
    elif lex == 'exportxlsx':
        print(export_xlsx())
    elif lex == 'add':
        add_num(arg)


def show():
    x = pt.PrettyTable()
    x.field_names = ["ID", "Номер телефона", "Имя", "e-mail"]
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()
    check_data = cur.execute("SELECT * FROM phone_book")
    all_res = check_data.fetchall()
    for i in all_res:
        x.add_row(i)
    return x

def add_num(x):
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS phone_book(
                    userid INT PRIMARY KEY,
                    phone_number TEXT,
                    name TEXT,
                    email TEXT);
                    """)
    conn.commit()

    number = tuple(x.split())

    cur.execute("INSERT INTO phone_book VALUES(?, ?, ?, ?);", number)
    conn.commit()

def delete_num(x):
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM phone_book WHERE phone_number = (?)", (x,))
    conn.commit()

def helper():
    return ("""=================================================================================================
Список команд и правила их правильного написания:
    add <id контакта(уникальный)> <номер телефона> <имя> <электронная почта> - добавить новый контакт
    exit - закончить работу в приложении
    help - показать этот список
    delete <id контакта> - удалить контакт
    show - показать список контактов
    exporttxt <путь к файлу> - произвести экспорт книги в файл .txt, аргумент path -  optional, default = "C://PhoneBook/"
    exportxlsx <путь к файлу> - произвести экспорт книги в файл .xlsx, аргумент path - optional, default = "C://PhoneBook/"
=================================================================================================
             """)

def fire_cloud(x):
    config = {
                "apiKey": "AIzaSyC5cQhsuam0IPWVeCD-h2XTnx77zaxoYZo",
                "authDomain": "phonebook-3538c.firebaseapp.com",
                "databaseURL": "https://phonebook-3538c-default-rtdb.europe-west1.firebasedatabase.app/",
                "storageBucket": "phonebook-3538c.appspot.com"
                }
    email, password = x[0], x[1]
    firebase = fb.Firebase(config)

def export_txt():
    path = "C://PhoneBook/"
    f = open(path + "phone_book.txt", 'w')
    f.write(show().get_string())
    f.close()
    return f"File successfully created in {path}"

def export_xlsx():
    path = "C://PhoneBook/"
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()
    check_data = cur.execute("SELECT * FROM phone_book")
    all_res = check_data.fetchall()
    data = pd.DataFrame(all_res)
    data.to_excel(path + "phone_book.xlsx", header = ["ID", "Номер телефона", "Имя", "e-mail"])
    return f"File successfully created in {path}"