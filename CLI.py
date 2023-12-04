# Command Line Interface Code
import sqlite3
from datetime import datetime # Know this package from my ECON 411 class


# Works & sucessfully checks for duplicate usernames
# potential add-ons: currently accepts blank entries, we should fix that
def new_user():
    conn1 = sqlite3.connect("twitterlike.db")
    success = False
    while success == False: # will allow menu repeat until successful creation 
        usernameInput = input("Make a username: ")
        query = conn1.cursor()
        query.execute("SELECT USERNAME FROM LOGININFO WHERE USERNAME = (?)", (usernameInput,))
        result = query.fetchall()
        if len(result) <= 0:
            passwordInput = input("Make a password: ")
            fullNameInput = input("Enter your full name: ")
            emailInput = input("Enter your email: ")
            profileImageInput = input("Select your profile image link: ")
            registrationDate = datetime.now()
            success = True
        else:
            print("Username already exists!")
            success = False
    userID = 0  
    cursor1 = conn1.execute("SELECT USERID FROM LOGININFO")
    for i in cursor1:
        userID += 1
    userID += 1
    conn1.execute("INSERT INTO LOGININFO \
                    VALUES (?, ?, ?, ?, ?, ?, ?)", (userID, usernameInput, passwordInput, fullNameInput, emailInput, profileImageInput, registrationDate))
    print("Successfully Registered!")
    conn1.commit()
    conn1.close()
    return userID


# works and checks for incorrect password combos and non-existant usernames
def login():
    conn1 = sqlite3.connect("twitterlike.db")
    usernameInput = input("Enter your username: ")
    query = conn1.cursor()
    query.execute("SELECT USERID, USERNAME, PASSWORD FROM LOGININFO WHERE USERNAME = (?)", (usernameInput,))
    result = query.fetchall()
    if len(result) != 0:
        userID = result[0][0]
        passwordInput = input("Enter your password: ")
        if result[0][2] == passwordInput:
            print("Successfully Logged In!")
        else:
            print("Incorrect Password")
            loginMenu()
    else:
        print("User not found.")
        loginMenu()
    conn1.close()
    return userID

# works, but will post empty tweets - the hashed if statement doesn't work
def postTweet(userID):
    print("Posting a Tweet")
    tweetText = ""
    while tweetText == "":
        tweetText = input("Enter your tweet: ")
        tweetText = tweetText.strip(" ")
    # if tweetText is not None:
    tweetChoice = int(input("Enter 1 if you want to post your tweet \nEnter 2 if you want to go back to the menu: "))
    if tweetChoice == 1:
        conn2 = sqlite3.connect("twitterlike.db")
        query = conn2.cursor()
        query.execute("SELECT TWEETID FROM TWEETS")
        result = query.fetchall()
        tweetID = len(result) + 1
        timeStamp = datetime.now()
        conn2.execute("INSERT INTO TWEETS (TWEETID, USERID, TWEET, TWEETTIME) \
                                VALUES (?, ?, ?, ?)", (tweetID, userID, tweetText, timeStamp))
        conn2.commit()
        conn2.close()
        tweetMenu(userID)
    elif tweetChoice == 2:
        tweetMenu(userID)
    else:
        print("Invalid choice. Please select a valid option.")
    # else:
    #     print ("Tweet can't be empty.")


# needs work, shows empty list right now.
# we need to make sure we are using SQL queries to make the list, not using loops to filter. TA was very specific about that
# I removed the like and comment options from the tweet menu. I think we should make them options under this instead so
# that the user will know the tweet ID 
def viewTimeline(userID):
    followed_users = []
    print("Viewing Timeline")
    conn3 = sqlite3.connect("twitterlike.db")
    cursor1 = conn3.execute("SELECT FOLLOWINGUSERID FROM FOLLOWT WHERE FOLLOWERUSERID = ?", (userID,))
    for followId in cursor1:
        print(followId)
        followed_users.append(followId[0])
    print(followed_users)
    # I think we need a JOIN SQL query here to make a table that has usernames (of all users followed), tweets and timestamps that we can then display as a list
    conn2 = sqlite3.connect("twitterlike.db")
    cursor2 = conn2.execute("SELECT * FROM TWEETS where USERID IN ({}) ORDER BY TWEETTIME DESC".format(','.join(map(str, followed_users))))
    for tweet in cursor2:
        tweet_id, user_id, tweet_content, creation_timestamp = tweet
        print("Tweet ID: {}, User ID: {}, Tweet Content: {}, Created At: {}".format(tweet_id, user_id, tweet_content, creation_timestamp))
    conn3.close()
    conn2.close()
    menuReturn = input('''Enter 1 if you want to return to the tweet menu \nEnter 2 to exit.''')
    if menuReturn == 1:
        tweetMenu()
    elif menuReturn == 2:
        print("Goodbye!")
        tweetMenu(userID)

# works, but output could look nicer
def tweetHistory(userID):
    print(f"Your Tweet History:")
    conn3 = sqlite3.connect("twitterlike.db")
    query = conn3.cursor()
    query.execute("SELECT TWEET,TWEETTIME FROM TWEETS WHERE USERID = ?", (userID,))
    tweetlist = query.fetchall()
    print(tweetlist)
    for tweet in tweetlist:
        print(f"Tweet: ", tweet[0], "Posted: ", tweet[1])
    conn3.close()
    menuReturn = input('''Enter 1 if you want to return to the tweet menu \n 
    Enter 2 to exit.''')
    if menuReturn == 1:
        tweetMenu()
    elif menuReturn == 2:
        print("Goodbye!")
        exit()


# works, needs error message if user is already following. SQL table is set up to throw error, just need python code to deal with it
def followUser(userID):
    print("Follow a User")
    followUserName = input("Enter the username you are looking for: ")
    conn1 = sqlite3.connect("twitterlike.db")
    query = conn1.cursor()
    query.execute("SELECT USERID, USERNAME FROM LOGININFO WHERE USERNAME = (?)", (followUserName,))
    fresult = query.fetchall()
    if fresult [0][1] == followUserName:
        followChoice = int(input(f"Enter 1 if you want to follow {followUserName} \nEnter 2 if you want to go back to the menu: "))
        if followChoice == 1:
            cursor2 = conn1.execute("SELECT COUNT(*) FROM FOLLOWT")
            result = cursor2.fetchone()
            followID = result[0] + 1
            followUserID = fresult [0][0]
            conn1.execute("INSERT INTO FOLLOWT (FOLLOWID, FOLLOWERUSERID, FOLLOWINGUSERID) \
                                    VALUES (?, ?, ?)", (followID, userID, followUserID))
            print(f"Successfully followed {followUserName}!")
            conn1.commit()
        elif followChoice == 2:
            tweetMenu(userID)
    conn1.close()
    menuReturn = int(input("Enter 1 if you want to return to the tweet menu \nEnter 2 to exit."))
    if menuReturn == 1:
        tweetMenu(userID)
    elif menuReturn == 2:
        print("Goodbye!")
        loginMenu()
    else:
        print("Invalid choice. Please select a valid option.")


# appears to work, needs more testing. Replaces connection with NULL values so it doesn't cause 
# problem with the count code for the followID 
# doesn't throw an error if you unfollow someone you don't already follow
def unfollowUser(userID):
    print("Unfollow a User")
    unfollowUsername = input("Enter the username you are looking for: ")
    conn1 = sqlite3.connect("twitterlike.db")
    query = conn1.cursor()
    query.execute("SELECT USERID, USERNAME FROM LOGININFO WHERE USERNAME = (?)", (unfollowUsername,))
    fresult = query.fetchall()
    if fresult [0][1] == unfollowUsername:
        unfollowChoice = int(input(f"Enter 1 if you want to unfollow {unfollowUsername} \nEnter 2 if you want to go back to the menu: "))
        if unfollowChoice == 1:
            unfollowUserID = fresult [0][0]
            conn1.execute('''UPDATE FOLLOWT SET FOLLOWERUSERID=NULL, FOLLOWINGUSERID=NULL WHERE 
                          FOLLOWERUSERID = (?) AND FOLLOWINGUSERID = (?)''', (userID, unfollowUserID))
            print(f"Successfully followed {unfollowUsername}!")
            conn1.commit()
        elif unfollowChoice == 2:
            tweetMenu(userID)
    conn1.close()
    menuReturn = int(input("Enter 1 if you want to return to the tweet menu \nEnter 2 to exit."))
    if menuReturn == 1:
        tweetMenu(userID)
    elif menuReturn == 2:
        print("Goodbye!")
        loginMenu()
    else: 
        print("Invalid choice. Please select a valid option.")

    

# needs work - how are the users supposed to know the tweet number?
# I removed the like and comment options from the tweet menu. I think we should make them options under this instead so
# that the user will know the tweet ID 
def likeTweet(tweetID):
    print("Liking a Tweet")
    tweetToLike = int(input("What tweet do you want to like (enter in number): "))
    conn2 = sqlite3.connect("twitterlike.db")
    cursor1 = conn2.execute("SELECT * FROM TWEETS")

    for row1 in cursor1:
        print(row1[0])
        print(tweetToLike)
        if row1[0] == tweetToLike:
            conn4 = sqlite3.connect("Table4")
            cursor2 = conn4.execute("SELECT COUNT(*) FROM LIKE")
            result = cursor2.fetchone()
            likeId = result[0]
            conn4.execute("INSERT INTO LIKE (LIKEID, LIKEUSERID, TWEETID) \
                                    VALUES (?, ?, ?)", (likeId, userId, tweetToLike))
            print("Tweet liked successfully!")
            conn4.commit()
            conn4.close()
    conn2.commit()
    conn2.close()

# needs work- how does the user know the tweet number? 
# I removed the like and comment options from the tweet menu. I think we should make them options under this instead so
# that the user will know the tweet ID 
def viewComments(tweetID):
    print("Viewing Tweet Comments")
    commentsOnTweet = int(input("What tweet do you want to see their comments (enter in number): "))
    conn5 = sqlite3.connect("twitterlike.db")
    cursor1 = conn5.execute("SELECT * FROM COMMENT WHERE TWEETID = ?", (commentsOnTweet,))
    cursor1 = cursor1.fetchall()
    if not cursor1:
            print("No Comments")
    else:
        for row in cursor1:
            print(f"Comment ID: {row[0]}, User ID: {row[1]}, Comment: {row[3]}, Comment Time: {row[4]}")

    conn5.commit()
    conn5.close()


def loginMenu():
    loginChoice = int(input("Enter 1 if you are making a new twitter account \nEnter 2 if you are logging in"))
    if loginChoice == 1:
        user = new_user()
        if user is not None:
            tweetMenu(user)

    elif loginChoice == 2:
        user = login()
        print(user)
        if user is not None:
            tweetMenu(user)
    else:
        print("Invalid choice. Please select a valid option.")



def tweetMenu(userID):

    print("Twitter-Like CLI Application")
    print("1. Post a Tweet")
    print("2. View Timeline")
    print("3. View Tweet History")
    print("4. Follow a User")
    print("5. Unfollow a User")
    print("6. Exit")

    menuChoice = int(input("Enter your choice (1 up to 7): "))

        # Works
    if menuChoice == 1:
        postTweet(userID)

            # Will have to adjust this code, found it on the internet because I was having difficulty figuring it out
    elif menuChoice == 2:
        viewTimeline(userID)
            
    # Works, will need an option for users to unlike a tweet (similar process to unfollowing a user)
    elif menuChoice == 3:
        tweetHistory(userID)

    # This function I believe works, but will have to include giving the user the option to add comments
    elif menuChoice == 4:
        followUser(userID)

    # Works
    elif menuChoice == 5:
        unfollowUser(userID)

    elif menuChoice == 6:
        print("Goodbye!")
        loginMenu()

    else:
        print("Invalid choice. Please select a valid option.")


loginMenu()




    