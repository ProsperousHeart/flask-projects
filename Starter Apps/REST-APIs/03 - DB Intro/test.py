# sqlite3 is part of python base install, still must import
import sqlite3

# create the sqlite connection - input param is the name of the DB
connection = sqlite3.connect('data.db')

# create cursor - think computer cursor
# allows you to select & start things
# responsible for executing queries
# (selection from, insert into, etc)
cursor = connection.cursor()

# create a table in SQL DB following schema (how it will look)
#   - STR is a SQL command (all caps)
#   - table name
#   - columns of table in (varname type, ...)
create_table = "CREATE TABLE users (id int, username text, password text)"

# run the query with the cursor
cursor.execute(create_table)
# if run the script now, a new file called "data.db" is created

# Let's store data for a single user!
user = (1, 'jose', 'asdf')
# Smart enough to know which pieces go with which ?
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# Let's add multiple users...
users = [
    (2, 'jan', 'hfds'),
    (3, 'jakob', 'jdd')
]
cursor.executemany(insert_query, users)

# Selecting users from a table...
select_query = "SELECT * FROM users"
# iterate over as if a list
for row in cursor.execute(select_query):
    print(row)

# Must tell connection to save all changes!
connection.commit()

# good practice to always...
connection.close()
# this way it doesn't receive any more data
# or consume resources while waiting
