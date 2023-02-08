import sqlite3

conn = sqlite3.connect('database.db')
print( "Opened database successfully")

conn.execute('''CREATE TABLE user (
    ID INTEGER PRIMARY KEY,
    num TEXT NOT NULL
);''')
print( "Table created successfully")
conn.close()