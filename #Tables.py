import sqlite3



conn = sqlite3.connect("Table1")

conn.execute('''
     CREATE TABLE LOGININFO
     (USERID    INT PRIMARY KEY,
     USERNAME   TEXT UNIQUE,
     PASSWORD   TEXT,
     FULLNAME   TEXT,
     EMAIL  TEXT,
     PROFILEIMAGE   TEXT,
     REGDATE    DATE); 
    ''')
conn.commit()



conn = sqlite3.connect("Table2")

conn.execute('''
     CREATE TABLE TWEETS
     (TWEETID   INT PRIMARY KEY UNIQUE,
      USERID    INT,
      TWEET TEXT,
      TWEETTIME     DATE); 
    ''')
conn.commit()



conn = sqlite3.connect("Table3")

conn.execute('''
     CREATE TABLE FOLLOWT
     (FOLLOWID   INT PRIMARY KEY UNIQUE,
      FOLLOWERUSERID    INT,
      FOLLOWINGUSERID    INT); 
    ''')
conn.commit()



conn = sqlite3.connect("Table4")

conn.execute('''
     CREATE TABLE LIKE
     (LIKEID   INT PRIMARY KEY UNIQUE,
      LIKEUSERID INT,
      TWEETID  TEXT); 
    ''')
conn.commit()



conn = sqlite3.connect("Table5")

conn.execute('''
     CREATE TABLE COMMENT
     (COMMENTID   INT PRIMARY KEY UNIQUE,
      COMMENTUSERID INT,
      TWEETID  TEXT,
      COMMENT   TEXT,
      COMMENTTIME   DATE); 
    ''')
conn.commit()

#test
conn.close()