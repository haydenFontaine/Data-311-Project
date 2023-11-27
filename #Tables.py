import sqlite3

conn = sqlite3.connect("Table1")

conn.execute('''
     CREATE TABLE LoginINFO
     (ID    INT PRIMARY KEY,
     USERNAME   TEXT UNIQUE,
     PASSWORD   TEXT,
     FULLNAME   TEXT,
     EMAIL  TEXT,
     PROFILEIMAGE   TEXT,
     REGDATE    DATE); 
    ''')
conn.commit()
conn.close()
