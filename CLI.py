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
            print("\nSuccessfully Logged In!\n")
        else:
            print("\nIncorrect Password\n")
            loginMenu()
    else:
        print("\nUser not found.\n")
        loginMenu()
    conn1.close()
    return userID

# works and cycles back if wrong choice entered
def postTweet(userID):
    print("Posting a Tweet\n")
    tweetText = ""
    while tweetText == "":
        tweetText = input("Enter your tweet: ")
        tweetText = tweetText.strip(" ")
    tweetposted = False
    while tweetposted == False:
        tweetChoice = int(input("Enter 1 if you want to post your tweet \nEnter 2 to discard tweet and go back to the menu: "))
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
            tweetposted = True
        elif tweetChoice == 2:
            tweetMenu(userID)
        else:
            print("\nInvalid choice. Please select a valid option.\n")
            tweetposted = False


# works, shows tweets of people the user follows
def viewTimeline(userID):
    print("Viewing Timeline\n")
    conn3 = sqlite3.connect("twitterlike.db")
    query = conn3.cursor()
    query.execute('''SELECT TWEETS.tweetid, TWEETS.userid, TWEETS.tweet, TWEETS.tweettime, FOLLOWT.followeruserid, 
                  FOLLOWT.followinguserid, LOGININFO.userid, LOGININFO.username FROM TWEETS inner JOIN FOLLOWT ON 
                  TWEETS.userid = FOLLOWT.followinguserid inner JOIN LOGININFO ON TWEETS.userid = LOGININFO.userid 
                  WHERE FOLLOWT.followeruserid = ? ORDER BY TWEETTIME''', (userID,))
    tweetlist = query.fetchall()
    listlength = len(tweetlist)
    if listlength >= 1:
        for i in range(0, listlength):
            print(f"\nTweet ID: ", tweetlist[i][0], " Tweet: ", tweetlist[i][2], "\nPosted By: ", tweetlist[i][6], " at ", tweetlist[i][3], "\n")
    else:
        print ("There are no tweets in your timeline. Add followers to fill your timeline!\n")
    tweetID = int(input("Enter Tweet ID for options. Enter 0 to go back to the menu: "))
    if tweetID == 0:
        tweetMenu(userID)
    else:
        try:
            query2 = conn3.cursor()
            query2.execute("SELECT TWEETID FROM TWEETS WHERE TWEETID = ?", (tweetID,))
            tweet = query2.fetchall()
            if tweet[0][0] == tweetID:
                commentlikeMenu(userID, tweetID)
            else: 
                print("Invalid Tweet ID. Try again!\n")
        except:
            print("Invalid Tweet ID. Try again!\n")

        
    # else:
    #     for j in range(0, listlength):
    #         if tweetlist[j][3] == tweetID:
    #             tweetfound = True
    #         else:
    #             tweetfound = False
    # if tweetfound == True:
    #     commentlikeMenu(userID, tweetID)
    # else:
        

# works
def tweetHistory(userID):
    print(f"Your Tweet History:\n")
    conn3 = sqlite3.connect("twitterlike.db")
    query = conn3.cursor()
    query.execute("SELECT TWEET,TWEETTIME FROM TWEETS WHERE USERID = ?", (userID,))
    tweetlist = query.fetchall()
    listlength = len(tweetlist)
    if listlength >= 1:
        for tweet in tweetlist:
            print(f"Tweet: ", tweet[0], "\nPosted: ", tweet[1], "\n")
    else:
        print("You haven't posted any tweets yet!\n")
    conn3.close()
    menuReturn = int(input("Enter 1 if you want to return to the Main Menu \nEnter 2 to exit."))
    if menuReturn == 1:
        tweetMenu(userID)
    elif menuReturn == 2:
        print("Goodbye!\n")
        loginMenu()


# works, needs error message if user is already following. SQL table is set up to throw error, just need python code to deal with it
def followUser(userID):
    print("Follow a User")
    followUserName = input("Enter the username you are looking for: ")
    conn1 = sqlite3.connect("twitterlike.db")
    query1 = conn1.cursor()
    query1.execute("SELECT USERID, USERNAME FROM LOGININFO WHERE USERNAME = (?)", (followUserName,))
    fresult = query1.fetchall()
    if fresult [0][1] == followUserName:
        followChoice = int(input(f"Enter 1 if you want to follow {followUserName} \nEnter 2 if you want to go back to the menu: "))
        if followChoice == 1:
            conn2 = sqlite3.connect("twitterlike.db")
            query = conn2.cursor()
            query.execute("SELECT * FROM FOLLOWT")
            result = query.fetchall()
            print(result)
            followID = len(result) + 1
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

    











# needs work - part of submenu for viewing timeline
def likeTweet(userID, tweetID):
    tracker = True
    tweetToLike = input("Liking a Tweet")
    conn2 = sqlite3.connect("twitterlike.db")
    cursor1 = conn2.execute("SELECT * FROM TWEETS")

    for row1 in cursor1:
        if row1[0] == tweetToLike:
            conn4 = sqlite3.connect("twitterlike.db")
            cursor2 = conn4.execute("SELECT COUNT(*) FROM LIKE")
            result = cursor2.fetchone()
            likeId = result[0]
            conn4.execute("INSERT INTO LIKE (LIKEID, LIKEUSERID, TWEETID) \
                                    VALUES (?, ?, ?)", (likeId, userID, tweetToLike))
            print("Tweet liked successfully!")
            conn4.commit()
            conn4.close()
        else:
            print(row1[2], row1[0], "Is not what is being looked for")
    #if tracker == True:
    #    print("you have already liked this")
    conn2.commit()
    conn2.close()
    tweetMenu(userID)

# needs work
def unlikeTweet(userID, tweetID):
    tracker = True
    tweetToLike = input("Liking a Tweet")
    conn2 = sqlite3.connect("twitterlike.db")
    cursor1 = conn2.execute("SELECT * FROM TWEETS")

    for row1 in cursor1:
        if tweetToLike == row1[0]:
            conn4 = sqlite3.connect("twitterlike.db")
            cursor2 = conn4.execute("SELECT COUNT(*) FROM LIKE")
            result = cursor2.fetchone()
            likeId = result[0]
            conn4.execute("DELETE LIKE WHERE TWEETID=(?) ",(tweetToLike))
            print("Tweet liked successfully!")
            conn4.commit()
            conn4.close()
        else:
            print(row1, "Is not what is being looked for")
    #if tracker == True:
    #    print("you have already liked this")
    conn2.commit()
    conn2.close()
    tweetMenu(userID)

# needs work
def addComment(userID, tweetID):
    pass

# needs testing 
def viewComments(userID, tweetID):
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
    loginChoice = int(input("Enter 1 if you are making a new twitter account \nEnter 2 if you are logging in \n"))
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
        print("Invalid choice. Please select a valid option.\n")



def tweetMenu(userID):

    print("Main Menu\n")
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
    elif menuChoice == 2:
        viewTimeline(userID)
    elif menuChoice == 3:
        tweetHistory(userID)
    elif menuChoice == 4:
        followUser(userID)
    elif menuChoice == 5:
        unfollowUser(userID)
    elif menuChoice == 6:
        print("Goodbye!")
        loginMenu()
    else:
        print("Invalid choice. Please select a valid option.")

        
def commentlikeMenu(userID, tweetID):
    conn3 = sqlite3.connect("twitterlike.db")
    query = conn3.cursor()
    query.execute("SELECT TWEET FROM TWEETS WHERE TWEETID = ?", (tweetID,))
    tweet = query.fetchone()

    print("\nTweet: ", tweet[0], "\n")
    print("1. Like Tweet")
    print("2. Unlike Tweet")
    print("3. Add Comment")
    print("4. View Comments")
    print("5. Return to Menu")
    print("6. Logout")

    menuChoice = int(input("Enter your choice (1 up to 6): "))
    if menuChoice == 1:
        likeTweet(userID, tweetID)
    elif menuChoice == 2:
        unlikeTweet(userID, tweetID)
    elif menuChoice == 3:
        addComment(userID, tweetID)
    elif menuChoice == 4:
        viewComments(userID, tweetID)
    elif menuChoice == 5:
        tweetMenu(userID)
    elif menuChoice == 6:
        print("Goodbye!")
        loginMenu
            


loginMenu()




    