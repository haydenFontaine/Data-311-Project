# Command Line Interface Code
import sqlite3
from datetime import datetime # Know this package from my ECON 411 class

userId = 0
tweetId = 0
followId = 0
likeId = 0

loginChoice = int(input("Enter 1 if you are making a new twitter account \
                    Enter 2 if you are logging in: "))

# Works
if loginChoice == 1:
    try:
        usernameInput = input("Make a username: ")
        passwordInput = input("Make a password: ")
        # fullNameInput = input("Enter your full name: ")
        # emailInput = input("Enter your email: ")
        # profileImageInput = input("Select your profile image: ")
        # registrationDate = datetime.now()

        conn1 = sqlite3.connect("Table1")
        cursor1 = conn1.execute("SELECT USERID FROM LOGININFO")
        for row in cursor1:
            userId += 1
        userId += 1
        conn1.execute("INSERT INTO LOGININFO (USERID, USERNAME, PASSWORD) \
                        VALUES (?, ?, ?)", (userId, usernameInput, passwordInput))
        # conn1.execute("INSERT INTO LOGININFO (USERID, USERNAME, PASSWORD, FULLNAME, EMAIL, PROFILEIMAGE, REGDATE) \
        #                 VALUES (?, ?, ?, ?, ?, ?, ?)", (userId, usernameInput, passwordInput, fullNameInput, emailInput, profileImageInput, registrationDate))
        print("Successfully Registered!")
        conn1.commit()
        conn1.close()

    except sqlite3.IntegrityError as err1:
        print("Username already exists!")

# Works
elif loginChoice == 2:
    conn1 = sqlite3.connect('Table1')
    cursor1 = conn1.execute("SELECT * FROM LOGININFO")

    usernameInput = input("Enter your username: ")
    passwordInput = input("Enter your password: ")

    for row in cursor1:
        if (row[1] == usernameInput) & (row[2] == passwordInput):
            print("Successfully Logged In!")
            loginUserId = row[0]

    conn1.close()

while True:
    print("Twitter-Like CLI Application")
    print("1. Post a Tweet")
    print("2. View Timeline")
    print("3. Like a Tweet")
    print("4. View Tweet Comments")
    print("5. Follow a User")
    print("6. Unfollow a User")
    print("7. Exit")

    menuChoice = int(input("Enter your choice (1 up to 7): "))

    # Works
    if menuChoice == 1:
        print("Posting a Tweet")
        tweetText = input("Enter your tweet: ")
        if tweetText is not None:
            tweetChoice = int(input("Enter 1 if you want to post your tweet \
                                    Enter 2 if you want to go back to the menu: "))
            if tweetChoice == 1:
                conn2 = sqlite3.connect("Table2")
                cursor1 = conn2.execute("SELECT COUNT(*) FROM TWEETS")
                result = cursor1.fetchone()
                tweetId = result[0]
                timeStamp = datetime.now()
                conn2.execute("INSERT INTO TWEETS (TWEETID, USERID, TWEET, TWEETTIME) \
                                         VALUES (?, ?, ?, ?)", (tweetId, userId, tweetText, timeStamp))
                conn2.commit()
                conn2.close()
            elif tweetChoice == 2:
                continue

    # Will have to adjust this code, found it on the internet because I was having difficulty figuring it out
    elif menuChoice == 2:
        followed_users = []
        print("Viewing Timeline")
        conn3 = sqlite3.connect("Table3")
        cursor1 = conn3.execute("SELECT FOLLOWINGUSERID FROM FOLLOWT WHERE FOLLOWERUSERID = ?", (userId,))
        for followId in cursor1:
            print(followId)
            followed_users.append(followId[0])
        print(followed_users)

        conn2 = sqlite3.connect("Table2")
        cursor2 = conn2.execute("SELECT * FROM TWEETS where USERID IN ({}) ORDER BY TWEETTIME DESC".format(','.join(map(str, followed_users))))
        for tweet in cursor2:
            tweet_id, user_id, tweet_content, creation_timestamp = tweet
            print("Tweet ID: {}, User ID: {}, Tweet Content: {}, Created At: {}".format(tweet_id, user_id, tweet_content, creation_timestamp))

        conn3.commit()
        conn3.close()
        conn2.commit()
        conn2.close()

    # Works, will need an option for users to unlike a tweet (similar process to unfollowing a user)
    elif menuChoice == 3:
        print("Liking a Tweet")
        tweetToLike = int(input("What tweet do you want to like (enter in number): "))
        conn2 = sqlite3.connect("Table2")
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

    # This function I believe works, but will have to include giving the user the option to add comments
    elif menuChoice == 4:
        print("Viewing Tweet Comments")
        commentsOnTweet = int(input("What tweet do you want to see their comments (enter in number): "))
        conn5 = sqlite3.connect("Table5")
        cursor1 = conn5.execute("SELECT * FROM COMMENT WHERE TWEETID = ?", (commentsOnTweet,))
        cursor1 = cursor1.fetchall()

        if not cursor1:
            print("No Comments")
        else:
            for row in cursor1:
                print(f"Comment ID: {row[0]}, User ID: {row[1]}, Comment: {row[3]}, Comment Time: {row[4]}")

        conn5.commit()
        conn5.close()

    # Works
    elif menuChoice == 5:
        print("Follow a User")
        followUserName = input("Enter the user you are looking for: ")
        conn1 = sqlite3.connect("Table1")
        cursor1 = conn1.execute("SELECT USERNAME, USERID FROM LOGININFO")

        for row in cursor1:
            if row[0] == followUserName:
                followUserId = row[1]
                followChoice = int(input(f"Enter 1 if you want to follow {followUserName} \
                                            Enter 2 if you want to go back to the menu: "))
                if followChoice == 1:
                    conn3 = sqlite3.connect("Table3")
                    cursor2 = conn3.execute("SELECT COUNT(*) FROM FOLLOWT")
                    result = cursor2.fetchone()
                    followId = result[0]
                    conn3.execute("INSERT INTO FOLLOWT (FOLLOWID, FOLLOWERUSERID, FOLLOWINGUSERID) \
                                            VALUES (?, ?, ?)", (followId, userId, followUserId))
                    print(f"Successfully followed {followUserName}!")
                    conn3.commit()
                    conn3.close()

                elif followChoice == 2:
                    continue
        conn1.commit()
        conn1.close()

    # Works
    elif menuChoice == 6:
        print("Unfollow a User")
        unfollowUserName = input("Enter the user you are looking for: ")
        conn1 = sqlite3.connect("Table1")
        cursor1 = conn1.execute("SELECT USERNAME, USERID FROM LOGININFO")

        for row1 in cursor1:
            if row1[0] == unfollowUserName:
                unfollowUserId = row1[1]
                conn3 = sqlite3.connect("Table3")
                cursor2 = conn3.execute("SELECT FOLLOWERUSERID, FOLLOWINGUSERID FROM FOLLOWT")
                for row2 in cursor2:
                    if row2[0] == userId and row2[1] == unfollowUserId:
                        unfollowChoice = int(input(f"Enter 1 if you want to unfollow {unfollowUserName} \
                                                            Enter 2 if you want to go back to the menu: "))
                        if unfollowChoice == 1:
                            unfollow = cursor2.execute(f"DELETE FROM FOLLOWT WHERE FOLLOWERUSERID = ?", (userId,))
                            print(f"Successfully unfollowed {unfollowUserName}!")

                        elif unfollowChoice == 2:
                            continue
                conn3.commit()
                conn3.close()

        conn1.commit()
        conn1.close()

    elif menuChoice == 7:
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please select a valid option.")





