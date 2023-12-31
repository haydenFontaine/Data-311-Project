# Tables Code
import sqlite3

conn = sqlite3.connect("twitterlike.db")

conn.execute('''
     CREATE TABLE LOGININFO
     (USERID    INT PRIMARY KEY UNIQUE,
     USERNAME   TEXT UNIQUE,
     PASSWORD   TEXT,
     FULLNAME   TEXT,
     EMAIL  TEXT,
     PROFILEIMAGE   TEXT,
     REGDATE    DATE); 
    ''')

conn.execute('''
     CREATE TABLE TWEETS
     (TWEETID INT PRIMARY KEY UNIQUE,
      USERID    INT,
      TWEET TEXT,
      TWEETTIME     DATE); 
      ''')

# added unique constraint to follower/following relationship to prevent duplicate relationships
conn.execute('''
     CREATE TABLE FOLLOWT
     (FOLLOWID   INT PRIMARY KEY UNIQUE,
      FOLLOWERUSERID    INT,
      FOLLOWINGUSERID    INT,
     UNIQUE(FOLLOWERUSERID, FOLLOWINGUSERID)
     );
    ''')


# added unique constraint to likeuserID/tweetID relationship to prevent duplicate relationships
conn.execute('''
     CREATE TABLE LIKE
     (LIKEID   INT PRIMARY KEY UNIQUE,
      LIKEUSERID INT,
      TWEETID  TEXT,
     UNIQUE (LIKEUSERID, TWEETID)
     ); 
      ''')

conn.execute('''
     CREATE TABLE COMMENT
     (COMMENTID   INT PRIMARY KEY UNIQUE,
      COMMENTUSERID INT,
      TWEETID  TEXT,
      COMMENT   TEXT,
      COMMENTTIME   DATE); 
    ''')
conn.commit()

conn.close()
