import sqlite3 as sql
import prettytable as pt
import pandas as pd
import pydrive as cloud

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
        print(delete_num(arg))
    elif lex == 'found':
        print(found(arg))
    elif lex == 'exporttxt':
        print(export_txt(arg))
    elif lex == 'exportxlsx':
        print(export_xlsx(arg))
    elif lex == 'add':
        print(add_num(arg))


def show():
    try:
        x = pt.PrettyTable()
        x.field_names = ["Номер телефона", "Имя", "e-mail"]
        conn = sql.connect("C://PhoneBook/phone_book.db")
        cur = conn.cursor()
        check_data = cur.execute("SELECT * FROM phone_book ORDER BY name ASC")
        all_res = check_data.fetchall()
        for i in all_res:
            x.add_row(i)
        return x
    except sql.OperationalError:
        create_table()
        show()

def add_num(x):
    conn, cur = create_table()

    number = tuple(x.split())

    cur.execute("SELECT * FROM phone_book WHERE phone_number = (?)", (number[0],))
    data = cur.fetchall()

    if len(data) != 0:
        return "This number already taken."
    cur.execute("INSERT INTO phone_book VALUES(?, ?, ?);", number)
    conn.commit()
    return "Successfully added."

def delete_num(x):
    try:
        conn = sql.connect("C://PhoneBook/phone_book.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM phone_book WHERE phone_number = (?)", (x,))
        conn.commit()
        return "Successfully deleted."
    except sql.OperationalError:
        create_table()
        delete_num(x)

def helper():
    return ("""=================================================================================================
Список команд и правила их правильного написания:
    add <номер телефона> <имя> <электронная почта> - добавить новый контакт
    exit - закончить работу в приложении
    help - показать этот список
    delete <номер контакта> - удалить контакт
    show - показать список контактов
    exporttxt <путь к файлу> - произвести экспорт книги в файл .txt, аргумент path -  optional, default = "C://PhoneBook/"
    exportxlsx <путь к файлу> - произвести экспорт книги в файл .xlsx, аргумент path - optional, default = "C://PhoneBook/"
    found <тип поиска(имя - name, номер - number или почта - mail)> <переменная для поиска> - найти контакты по заданному критерию
=================================================================================================
             """)

def export_txt(path):
    if len(path) != 0:
        try:
            f = open(path + "phone_book.txt", 'w')
            f.write(show().get_string())
            f.close()
            return f"File successfully created in {path}"
        except PermissionError:
            return "This path is unaviable. Try to use another path"
    path = "C://PhoneBook/"
    f = open(path + "phone_book.txt", 'w')
    f.write(show().get_string())
    f.close()
    return f"File successfully created in {path}"

def export_xlsx(path):
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()
    check_data = cur.execute("SELECT * FROM phone_book")
    all_res = check_data.fetchall()
    data = pd.DataFrame(all_res)

    if len(path) != 0:
        try:
            data.to_excel(path + "phone_book.xlsx", header = ["Номер телефона", "Имя", "e-mail"])
            return f"File successfully created in {path}"
        except PermissionError:
            return "This path is unaviable. Try to use another path"
    path = "C://PhoneBook/"
    data.to_excel(path + "phone_book.xlsx", header = ["Номер телефона", "Имя", "e-mail"])
    return f"File successfully created in {path}"

def create_table():
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
    zapros = x.split()
    if zapros[0] == 'name':
        return found_name(zapros[1])
    elif zapros[0] == 'number':
        return found_num(zapros[1])
    elif zapros[0] == 'mail':
        return found_mail(zapros[1])
    else:
        return "Error: Unexpected argument for type."

def found_name(x):
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
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM phone_book WHERE phone_number = (?)", (x,))
    data = cur.fetchall()

    y = pt.PrettyTable()
    y.field_names = ["Номер телефона", "Имя", "e-mail"]

    for i in data:
        y.add_row(i)

    return y

def found_mail(x):
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM phone_book WHERE email = (?)", (x,))
    data = cur.fetchall()

    y = pt.PrettyTable()
    y.field_names = ["Номер телефона", "Имя", "e-mail"]

    for i in data:
        y.add_row(i)

    return y


#def login(x):
    #login, password = x.split