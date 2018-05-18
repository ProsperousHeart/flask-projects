import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# id will start at 1
# create_tbl_query = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text)"
create_tbl_query = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_tbl_query)

# create new table for items
# create_tbl_query = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
create_tbl_query = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_tbl_query)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")
# no longer needed now that we have ability to add to DB

connection.commit()
connection.close()
