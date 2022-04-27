import sqlite3 as sql

def lexer(c):       # ����������� �������, ������� ����� ���������
                    # ��������� ������ �� ������� � ��������
    lex = ''        # �������
    arg = ''        # ��������
    l = True        # ������ � ������� ��� � ��������?
    for i in c:
        if i == ' ' and l:
            l = False       # ������ ����� ������ � ��������
        elif l:
            lex += i 
        else:
            arg += i
    return shell(lex,arg)


def shell(lex,arg):         # �������������
    if lex == 'echo':
        print(arg)
    elif lex == 'exit':
        return True
    elif lex == 'show_book':
        print(show(arg))
    elif lex == 'add':
        add_num(arg)


def show(arg):
    conn = sql.connect("C://PhoneBook/phone_book.db")
    cur = conn.cursor()
    check_data = cur.execute("SELECT * FROM phone_book")
    all_res = check_data.fetchall()
    return len(all_res)

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