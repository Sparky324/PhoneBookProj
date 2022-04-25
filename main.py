import create_logic as cl


PATH = "C://PhoneBook"
FILE_NAME = "phone_book.db"


print(cl.create_directory(PATH))
print(cl.create_db(FILE_NAME, PATH))