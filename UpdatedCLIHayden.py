# Command Line Interface Code
import sqlite3
from datetime import datetime  # Know this package from my ECON 411 class

"""After troubleshooting, work I believe that has to be done:
1) Add remove comments function - I don't think this is necessary (Kristen)
2) Make sure that all ids are properly incremented, and keeping it consistent across all ids (ex: userID may start at 1, 
should be same for likeID for consistency - I checked them to make sure they are all counting the same way, 
so they should be consistent now (Kristen)
3) More troubleshooting and error handling. I believe I got most of them (main concern is with unfollow user, 
see comments above function). - Fixed (Kristen)"""

# Works & successfully checks for duplicate usernames
# potential add-ons: currently accepts blank entries, we should fix that (fixed blank entries: Hayden)
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

            # Decided to include blank entries on profile image, as social media normally doesn't require you to have a profile image, and has a default one (Hayden)
            profileImageInput = input("Select your profile image link: ")
            registrationDate = datetime.now()
            success = True
        else:
            print("Username already exists or you have entered no username. Try again!")
            success = False

    query2 = conn.cursor()
    query2.execute("SELECT USERID FROM LOGININFO")
    userIDs = query2.fetchall()
    userID = len(userIDs) +1
    query3 = conn.cursor()
    query3.execute("INSERT INTO LOGININFO \
                    VALUES (?, ?, ?, ?, ?, ?, ?)", (userID, usernameInput, passwordInput, fullNameInput, emailInput, profileImageInput, registrationDate))
    print("Successfully Registered!")
    conn.commit()
    conn.close()
    return userID


# works and checks for incorrect password combos and non-existant usernames
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


# works and cycles back if wrong choice entered
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
            conn.commit()
            conn.close()
            tweetMenu(userID)
            tweetPosted = True
        elif tweetChoice == 2:
            tweetMenu(userID)
        else:
            print("\nInvalid choice. Please select a valid option.\n")
            tweetPosted = False


# works, shows tweets of people the user follows
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

# works
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
        print("Goodbye!\n")
        loginMenu()


# works, needs error message if user is already following. SQL table is set up to throw error, just need python code to deal with 
# it (fixed: Hayden)
def followUser(userID):
    print("Follow a User")
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

# I believe it works, accounting for if username is not found or if user is not following the username they were looking for. 
# Will have to double checking if the ID counts are correct,
# also occasionally there is an operationalerror that occurs where it says database is locked. Not sure how we would fix that. 
# (Hayden). I think it was becuase the conn.commit() line was inside the if function. I moved it outside (Kristen)
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

# Troubleshooted it, and I believe it works now -Hayden
# tested and found no erros (Kristen)
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
            likeID = tResult[0] +1

            query4 = conn.cursor()
            query4.execute("INSERT INTO LIKE (LIKEID, LIKEUSERID, TWEETID) VALUES (?,?,?)",
                            (likeID, userID, tweetID))
            print("Tweet liked successfully!")
            conn.commit()
        else:
            print("Tweet not found.")

    conn.close()
    viewTimeline(userID)


# Should work now -Hayden
# fixed delete to change to NULL, otherwise it throws error when next user tries to like a tweet
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

# Works now -Hayden
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
        viewTimeline(userID)
    elif commentChoice == 2:
        tweetMenu(userID)
    else:
        print("\nInvalid choice. Please select a valid option.\n")
        tweetMenu(userID)

# works, cleaned up display (Kristen)
def viewComments(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")
    query1 = conn.cursor()
    query1.execute('''SELECT TWEETS.TWEETID, TWEETS.TWEET, TWEETS.USERID, LOGININFO.USERID, LOGININFO.USERNAME FROM TWEETS 
                   JOIN LOGININFO ON TWEETS.USERID = LOGININFO.USERID where TWEETS.TWEETID = ?''', (tweetID,))
    tweet = query1.fetchall()
    print(tweet)
    print(f"Viewing Tweet Comments for {tweet[0][1]}\n")
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


def loginMenu():
    try:
        loginChoice = int(input("Enter 1 if you are making a new twitter account \nEnter 2 if you are logging in \n"))
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
            print("Logging out!")
            loginMenu()
        elif menuChoice == 7:
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")
            tweetMenu()


def commentlikeMenu(userID, tweetID):
    conn = sqlite3.connect("twitterlike.db")
    query = conn.cursor()
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
        print("Logging out...")
        loginMenu()
    else:
        print("Invalid choice. Please select a valid option.")
        commentlikeMenu(userID,tweetID)

loginMenu()




