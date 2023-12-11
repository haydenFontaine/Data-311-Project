# Command Line Interface Code
import sqlite3
from datetime import datetime  # Note to TA/Professor: Hayden learned how to use this package from another coding course

"""
Function: new_user
Arguments: None
Purpose: Registers a new user and stores their information into the database. Connects to the database, and requires for users to submit a unique and non-blank username, password,
full name, and email. Profile picture is optional due to most social media accounts having a default profile image. The time of registration is recorded and stored, along with a 
uniquely generated userID. 
"""
def new_user():
    conn = sqlite3.connect("twitterlike.db")
    success = False
    while not success:  # will allow menu repeat until successful creation
        usernameInput = input("Make a username: ")
        usernameInputCheck = usernameInput.strip()
        while usernameInputCheck == "":
            usernameInput = input("Entered no username, try again. Enter your username: ")
            usernameInputCheck = usernameInput.strip()
        query1 = conn.cursor()
        query1.execute("SELECT USERNAME FROM LOGININFO WHERE USERNAME = (?)", (usernameInput,))
        result = query1.fetchall()
        if len(result) <= 0:
            passwordInput = input("Make a password: ")
            passwordInputCheck = passwordInput.strip()
            while passwordInputCheck == "":
                passwordInput = input("Entered no password, try again. Enter your password: ")
                passwordInputCheck = passwordInput.strip()

            fullNameInput = input("Enter your full name: ")
            fullNameInputCheck = fullNameInput.strip()
            while fullNameInputCheck == "":
                fullNameInput = input("Entered no name, try again. Enter your full name: ")
                fullNameInputCheck = fullNameInput.strip()

            emailInput = input("Enter your email: ")
            emailInputCheck = emailInput.strip()
            while emailInputCheck == "":
                emailInput = input("Entered no email, try again. Enter your email: ")
                emailInputCheck = emailInput.strip()

            profileImageInput = input("Select your profile image link: ")
            registrationDate = datetime.now()
            success = True
        else:
            print("Username already exists or you have entered no username. Try again!")
            success = False

    query2 = conn.cursor()
    query2.execute("SELECT USERID FROM LOGININFO")
    userIDs = query2.fetchall()
    userID = len(userIDs) + 1
    query3 = conn.cursor()
    query3.execute("INSERT INTO LOGININFO \
                    VALUES (?, ?, ?, ?, ?, ?, ?)", (userID, usernameInput, passwordInput, fullNameInput, emailInput, profileImageInput, registrationDate))
    print("Successfully Registered!")
    conn.commit()
    conn.close()
    return userID


"""
Function: login
Arguments: None
Purpose: To login a user to their account, requiring the username and password of their account. Selects the userID, username, and password from the database and verifies that it belongs
to an existing account in the database.
"""
def login():
    conn = sqlite3.connect("twitterlike.db")
    usernameInput = input("Enter your username: ")
    query = conn.cursor()
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
    conn.close()
    return userID


"""
Function: postTweet
Arguments: userID (the unique ID associated with each account in the database)
Purpose: Allows the user to enter a tweet they would like to post, verify if they want to do so, and stores the tweet into the database. The tweet in the database contains the unique ID
with each tweet, the unique user ID, the text of the tweet that is being posted, and the time on when the tweet was posted.
"""
def postTweet(userID):
    print("Posting a Tweet\n")
    tweetText = ""
    while tweetText == "":
        tweetText = input("Enter your tweet: ")
        tweetText = tweetText.strip(" ")
    tweetPosted = False
    while not tweetPosted:
        tweetChoice = int(input("Enter 1 if you want to post your tweet \nEnter 2 to discard tweet and go back to the menu: "))
        if tweetChoice == 1:
            conn = sqlite3.connect("twitterlike.db")
            query1 = conn.cursor()
            query1.execute("SELECT TWEETID FROM TWEETS")
            result = query1.fetchall()
            tweetID = len(result) + 1
            timeStamp = datetime.now()

            query2 = conn.cursor()
            query2.execute("INSERT INTO TWEETS (TWEETID, USERID, TWEET, TWEETTIME) \
                                    VALUES (?, ?, ?, ?)", (tweetID, userID, tweetText, timeStamp))
            print("Tweet Posted!")
            conn.commit()
            conn.close()
            tweetMenu(userID)
            tweetPosted = True
        elif tweetChoice == 2:
            tweetMenu(userID)
        else:
            print("\nInvalid choice. Please select a valid option.\n")
            tweetPosted = False

"""
Function: viewTimeline
Arguments: userID (the unique ID associated with each account in the database)
Purpose: Allows the user to view their twitter timeline, consisting of the tweets of the accounts that the user follows. The unique tweet ID is shown, along with the text of the tweet,
who it was posted by, and the time of the tweet being posted. This was completed by connecting to the database, and creating a comprehensive table using a double join, organizing tweets
by the time of posting. The user can enter in the unique tweet ID to open the comment/like menu if it exists.
"""
def viewTimeline(userID):
    print("\nViewing Timeline\n")
    conn = sqlite3.connect("twitterlike.db")
    query1 = conn.cursor()
    query1.execute('''SELECT TWEETS.tweetid, TWEETS.userid, TWEETS.tweet, TWEETS.tweettime, FOLLOWT.followeruserid, 
                  FOLLOWT.followinguserid, LOGININFO.userid, LOGININFO.username FROM TWEETS inner JOIN FOLLOWT ON 
                  TWEETS.userid = FOLLOWT.followinguserid inner JOIN LOGININFO ON TWEETS.userid = LOGININFO.userid 
                  WHERE FOLLOWT.followeruserid = ? ORDER BY TWEETTIME''', (userID,))
    tweetList = query1.fetchall()
    listLength = len(tweetList)
    if listLength >= 1:
        for i in range(0, listLength):
            print(f"\nTweet ID: ", tweetList[i][0], " Tweet: ", tweetList[i][2], "\nPosted By: ", tweetList[i][7],
                  " at ", tweetList[i][3], "\n")
    else:
        print("There are no tweets in your timeline. Add followers to fill your timeline!\n")
    tweetID = int(input("Enter Tweet ID for options. Enter 0 to go back to the menu: "))
    if tweetID == 0:
        tweetMenu(userID)
    else:
        try:
            query2 = conn.cursor()
            query2.execute("SELECT TWEETID FROM TWEETS WHERE TWEETID = ?", (tweetID,))
            tweet = query2.fetchall()
            if tweet[0][0] == tweetID:
                commentlikeMenu(userID, tweetID)
            else:
                print("Invalid Tweet ID. Try again!\n")
        except IndexError as tweetIDError:
            print("Invalid Tweet ID. Try again!\n")

"""
Function: tweetHistory
Arguments: userID (the unique ID associated with each account in the database)
Purpose: Allows the user to view the tweets they have posted, and the date of posting if they have any. Gives the user the option to return to the main menu or to logout.
"""
def tweetHistory(userID):
    print(f"Your Tweet History:\n")
    conn = sqlite3.connect("twitterlike.db")
    query = conn.cursor()
    query.execute("SELECT TWEET,TWEETTIME FROM TWEETS WHERE USERID = ?", (userID,))
    tweetList = query.fetchall()
    listLength = len(tweetList)
    if listLength >= 1:
        for tweet in tweetList:
            print(f"Tweet: ", tweet[0], "\nPosted: ", tweet[1], "\n")
    else:
        print("You haven't posted any tweets yet!\n")
    conn.close()
    menuReturn = int(input("Enter 1 if you want to return to the Main Menu \nEnter 2 to logout."))
    if menuReturn == 1:
        tweetMenu(userID)
    elif menuReturn == 2:
        print("Logging out...\n")
        loginMenu()


"""
Function: followUser
Arguments: userID (the unique ID associated with each account in the database)
Purpose: Enables the user to follow another account, given that the username entered exists or they aren't already following the account. If the username entered doesn't exists or 
they already follow the account, returns the user directly to the main menu. Once a username is entered, confirms with the user if they want to follow that account, otherwise it returns 
them to the main menu. The information that's stored after the user follows another account are both users ID's, along with a unique followID. 
"""
def followUser(userID):
    print("Follow a User\n")
    followUserName = input("Enter the username you are looking for: ")
    conn = sqlite3.connect("twitterlike.db")
    query1 = conn.cursor()
    query1.execute("SELECT USERID, USERNAME FROM LOGININFO WHERE USERNAME = (?)", (followUserName,))
    fResult = query1.fetchall()
    try:
        if fResult[0][1] == followUserName:
            followChoice = int(
                input(f"Enter 1 if you want to follow {followUserName} \nEnter 2 if you want to go back to the menu: "))
            try:
                if followChoice == 1:
                    query2 = conn.cursor()
                    query2.execute("SELECT * FROM FOLLOWT")
                    result = query2.fetchall()
                    followID = len(result) + 1
                    followUserID = fResult[0][0]
                    query3 = conn.cursor()
                    query3.execute("INSERT INTO FOLLOWT (FOLLOWID, FOLLOWERUSERID, FOLLOWINGUSERID) \
                                    VALUES (?, ?, ?)", (followID, userID, followUserID))
                    print(f"Successfully followed {followUserName}!")
                    conn.commit()
                elif followChoice == 2:
                    tweetMenu(userID)
            except sqlite3.IntegrityError as alreadyFollowingUser:
                print("You are already following that user. Going back to main menu.")
                tweetMenu(userID)
    except IndexError as noExistingUser:
        print("Can't find username. Going back to main menu.")
        tweetMenu(userID)
    conn.close()

"""
Function: unfollowUser
Arguments: userID (the unique ID associated with each account)
Purpose: Unfollows an account, given that the account exists in the database and the current user is following that account. If the account doesn't exist or the user doesn't follow the 
account, return the user to the main menu. Once a username is entered, confirms with the user if they want to follow that account, otherwise it returns them to the main menu. The information
in the database is updated then to a NULL value, as opposed to deleting to prevent any issues with incrementing unique followID's.
"""
def unfollowUser(userID):
    print("Unfollow a User")
    unfollowUsername = input("Enter the username you are looking for: ")
    conn = sqlite3.connect("twitterlike.db")
    query1 = conn.cursor()
    query1.execute("SELECT USERID, USERNAME FROM LOGININFO WHERE USERNAME = (?)", (unfollowUsername,))
    fResult = query1.fetchall()
    if not fResult:
        print("Username not found. Going back to main menu.")
        conn.close()
        tweetMenu(userID)
    elif fResult[0][1] == unfollowUsername:
        query2 = conn.cursor()
        query2.execute("SELECT FOLLOWERUSERID, FOLLOWINGUSERID FROM FOLLOWT WHERE FOLLOWERUSERID = (?) and FOLLOWINGUSERID = (?)", (userID, fResult[0][0]))
        fResult = query2.fetchall()

        if fResult:
            unfollowChoice = int(input(f"Enter 1 if you want to unfollow {unfollowUsername} \nEnter 2 if you want to go back to the main menu: "))
            if unfollowChoice == 1:
                unfollowUserID = fResult[0][0]
                query3 = conn.cursor()
                query3.execute('''UPDATE FOLLOWT SET FOLLOWERUSERID=NULL, FOLLOWINGUSERID=NULL WHERE 
                          FOLLOWERUSERID = (?) AND FOLLOWINGUSERID = (?)''', (userID, unfollowUserID))
                print(f"Successfully unfollowed {unfollowUsername}!")
            elif unfollowChoice == 2:
                tweetMenu(userID)
        else:
            print("You are not following that user. Going back to main menu.")
            tweetMenu(userID)
        conn.commit()

"""
Function: likeTweet
Arguments: userID (the unique ID associated with each account), tweetID (the unique ID associated with each individual tweet)
Purpose: Checks if the user already liked the tweet, and then adds a like to the tweet, entering the unique likeID, userID, and tweetID into the database. Once the tweet is liked, returns
the user back to the main menu.
"""
def likeTweet(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")
    query1 = conn.cursor()
    query1.execute("SELECT * FROM LIKE WHERE LIKEUSERID = ? and TWEETID = ?", (userID, tweetID))
    existing_like = query1.fetchone()

    if existing_like:
        print("You have already liked this tweet.")

    else:
        query2 = conn.cursor()
        query2.execute("SELECT * FROM TWEETS WHERE TWEETID = ?", (tweetID,))
        existing_tweet = query2.fetchone()

        if existing_tweet:
            query3 = conn.cursor()
            query3.execute("SELECT COUNT(*) FROM LIKE")
            tResult = query3.fetchone()
            likeID = tResult[0] + 1

            query4 = conn.cursor()
            query4.execute("INSERT INTO LIKE (LIKEID, LIKEUSERID, TWEETID) VALUES (?,?,?)",
                            (likeID, userID, tweetID))
            print("Tweet liked successfully!")
            conn.commit()
        else:
            print("Tweet not found.")

    conn.close()
    tweetMenu(userID)


"""
Function: unlikeTweet
Arguments: userID (the unique ID associated with each account), tweetID (the unique ID associated with each individual tweet)
Purpose: Checks if the user has liked the tweet or has already unliked it, and then unlikes the tweets, replacing the values in the database to NULL to prevent issues with incrementing
likeID's. Once the tweet is unliked, returns the user to the main menu.
"""
def unlikeTweet(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")

    query1 = conn.cursor()
    query1.execute("SELECT * FROM LIKE WHERE LIKEUSERID = ? and TWEETID = ?", (userID, tweetID))
    existing_like_on_tweet = query1.fetchone()

    if not existing_like_on_tweet:
        print("You have not liked this tweet or have already unliked it.")

    else:
        query2 = conn.cursor()
        query2.execute("SELECT * FROM TWEETS WHERE TWEETID = ?", (tweetID,))
        existing_tweet = query2.fetchone()

        if existing_tweet:
            query3 = conn.cursor()
            query3.execute("UPDATE LIKE SET LIKEUSERID=NULL, TWEETID=NULL WHERE LIKEUSERID = ? AND TWEETID = ?", (userID, tweetID))
            print("Tweet unliked successfully!")

            query4 = conn.cursor()
            query4.execute("SELECT COUNT(*) FROM LIKE")
            result = query4.fetchone()
            likeID = result[0]
            conn.commit()
        else:
            print("Tweet not found.")

    conn.close()
    tweetMenu(userID)

"""
Function: viewLikes
Arguments: userID (the unique ID associated with each account), tweetID (the unique ID associated with each individual tweet)
Purpose: Selects the tweet that is equal to the tweetID inputted, displays the tweet and the user that created the tweet, and displays the likes if there is any. Returns the user to the main
menu.
"""
def viewLikes(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")
    query1 = conn.cursor()
    query1.execute('''SELECT TWEETS.TWEETID, TWEETS.TWEET, TWEETS.USERID, LOGININFO.USERID, LOGININFO.USERNAME FROM TWEETS 
                   JOIN LOGININFO ON TWEETS.USERID = LOGININFO.USERID WHERE TWEETS.TWEETID = ?''', (tweetID,))
    tweet = query1.fetchall()
    print(f"Tweet: {tweet[0][1]} by {tweet[0][4]}")
    query2 = conn.cursor()
    query2.execute("SELECT LIKEID FROM LIKE WHERE TWEETID = ?", (tweetID,))
    likes = query2.fetchall()
    like_count = len(likes)
    if like_count == 0:
        print("No Likes")
    else:
        print(f"Likes: {like_count}")
    conn.close()
    tweetMenu(userID)


"""
Function: addComment
Arguments: userID (the unique ID associated with each account), tweetID (the unique ID associated with each individual tweet)
Purpose: Allows the user to submit a comment to a tweet that was selected, given the comment is not empty. Confirms with the user if they want to post the comment, and then inserts
the comment, having a unique commentID, the ID of the user entering the comment, the tweetID associated with the tweet being commented on, the comment itself, and the time the comment
was made. Returns the user to the main menu.
"""
def addComment(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")

    commentOnTweet = input("Enter your comment: ")
    commentOnTweet = commentOnTweet.strip()
    while commentOnTweet == "":
        commentOnTweet = input("Empty comment, re-enter your comment: ")

    commentChoice = int(input("Enter 1 if you want to post your comment \nEnter 2 to discard tweet and go back to the menu: "))
    if commentChoice == 1:
        query1 = conn.cursor()
        query1.execute("SELECT COMMENTID FROM COMMENT")
        result = query1.fetchall()
        commentID = len(result) + 1
        commentTimeStamp = datetime.now()

        query2 = conn.cursor()
        query2.execute("INSERT INTO COMMENT (COMMENTID, COMMENTUSERID, TWEETID, COMMENT, COMMENTTIME) \
                                       VALUES (?, ?, ?, ?,?)", (commentID, userID, tweetID, commentOnTweet, commentTimeStamp))
        conn.commit()
        conn.close()
        tweetMenu(userID)
    elif commentChoice == 2:
        tweetMenu(userID)
    else:
        print("\nInvalid choice. Please select a valid option.\n")
        tweetMenu(userID)

"""
Function: viewComments
Arguments: userID (the unique ID associated with each account), tweetID (the unique ID associated with each individual tweet)
Purpose: Views all the comments for the selected tweet, given that there are existing comments on the tweet. Displays each comment, along with the username of the person that submitted
the comment, and the time the comment was made. Returns the user to the main menu.
"""
def viewComments(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")
    query1 = conn.cursor()
    query1.execute('''SELECT TWEETS.TWEETID, TWEETS.TWEET, TWEETS.USERID, LOGININFO.USERID, LOGININFO.USERNAME FROM TWEETS 
                   JOIN LOGININFO ON TWEETS.USERID = LOGININFO.USERID where TWEETS.TWEETID = ?''', (tweetID,))
    tweet = query1.fetchall()
    print(f"Viewing Tweet Comments for {tweet[0][1]}\n by {tweet[0][4]}")
    query2 = conn.cursor()
    query2.execute('''SELECT COMMENT.COMMENT, COMMENT.COMMENTUSERID, COMMENT.COMMENTTIME, LOGININFO.USERID, LOGININFO.USERNAME 
                   FROM COMMENT JOIN LOGININFO ON COMMENT.COMMENTUSERID = LOGININFO.USERID WHERE TWEETID = ?''', (tweetID,))
    existing_comments = query2.fetchall()
    if not existing_comments:
        print("No Comments")
    else:
        for comment_info in existing_comments:
            print(f"Comment: {comment_info[0]} by {comment_info[4]} at {comment_info[2]}")
    conn.close()
    tweetMenu(userID)

"""
Function: loginMenu
Arguments: None
Purpose: Creates a initial menu that prompts users if they are making a new account or logging in. Calls the function new_user if the user is making a new account, and calls the function
login if the user is logging in, and prompts them again if they select another option or exits the application if an error is thrown. If an ID exists/is created with the account, the program
continues to the main menu.
"""

def loginMenu():
    try:
        loginChoice = int(input("\nEnter 1 if you are making a new twitter account \nEnter 2 if you are logging in \n"))
        if loginChoice == 1:
            user = new_user()
            if user is not None:
                tweetMenu(user)

        elif loginChoice == 2:
            user = login()
            if user is not None:
                tweetMenu(user)
        else:
            print("Invalid choice. Please select a valid option.\n")
            loginMenu()
    except ValueError as err:
        print("Can only enter a whole number/real value. Restart application and try again.\n")
        exit()

"""
Function: tweetMenu
Arguments: userID (the unique ID associated with each account)
Purpose: Creates the main menu for the user to interact with upon logging in/registering for a twitter account. Prompts the user to enter in their choice based on 7 options, and calls the 
function associated with the user's choice. Prompts the user again to make a selection if they make an invalid choice.
"""
def tweetMenu(userID):
    selection = True
    while selection:
        print("\nMain Menu\n")
        print("1. Post a Tweet")
        print("2. View Timeline")
        print("3. View Tweet History")
        print("4. Follow a User")
        print("5. Unfollow a User")
        print("6. Logout")
        print("7. Exit Application")

        menuChoice = int(input("\nEnter your choice (1 up to 7): "))

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
            print("Logging out!")
            loginMenu()
        elif menuChoice == 7:
            print("Goodbye!")
            exit()
        else:
            print("\nInvalid choice. Please select a valid option.")
            tweetMenu(userID)

"""
Function: commentlikeMenu
Arguments: userID (the ID associated with each account), tweetID (the ID associated with each individual tweet)
Purpose: Create a menu where, for a given tweet ID, shows the tweet and prompts the user to enter in their selected choice out of 7 options. Calls the function associated with the 
user's choice, and prompts the user again if they make an invalid choice.
"""
def commentlikeMenu(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")
    query = conn.cursor()
    query.execute("SELECT TWEET FROM TWEETS WHERE TWEETID = ?", (tweetID,))
    tweet = query.fetchone()

    print("\nTweet: ", tweet[0], "\n")
    print("1. Like Tweet")
    print("2. Unlike Tweet")
    print("3. View Likes")
    print("4. Add Comment")
    print("5. View Comments")
    print("6. Return to Menu")
    print("7. Logout")

    menuChoice = int(input("\nEnter your choice (1 up to 7): "))
    if menuChoice == 1:
        likeTweet(userID, tweetID)
    elif menuChoice == 2:
        unlikeTweet(userID, tweetID)
    elif menuChoice == 3:
        viewLikes(userID, tweetID)
    elif menuChoice == 4:
        addComment(userID, tweetID)
    elif menuChoice == 5:
        viewComments(userID, tweetID)
    elif menuChoice == 6:
        tweetMenu(userID)
    elif menuChoice == 7:
        print("\nLogging out...")
        loginMenu()
    else:
        print("\nInvalid choice. Please select a valid option.")
        commentlikeMenu(userID, tweetID)

loginMenu()
