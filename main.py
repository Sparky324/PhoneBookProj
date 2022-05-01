import create_logic as cl
import functions as fc
import os

PATH = "C://PhoneBook"
FILE_NAME = "phone_book.db"


print(cl.create_directory(PATH))
print(cl.create_db(FILE_NAME, PATH))

print("""=========>Добро пожаловать в Телефонную Книгу!<=========
""")

while True:
    com = input("Enter your command ==> ")
    if fc.lexer(com): 
        break 