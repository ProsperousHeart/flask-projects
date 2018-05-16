import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# id will start at 1
# create_tbl_query = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text)"
create_tbl_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_tbl_query)

connection.commit()
connection.close()
