import sqlite3

conn = sqlite3.connect('database.db')
print( "Opened database successfully")

conn.execute('''CREATE TABLE user (
    ID INTEGER PRIMARY KEY,
    num TEXT NOT NULL,
    visit_time TIMESTAMP,
    eschar FLOAT,
    slough FLOAT,
    granulation FLOAT,
    area FLOAT,
    img BLOB
);''')
print( "Table created successfully")
conn.close()