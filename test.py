import sqlite3
import sys
import getpass
import uuid
import time

connection = None
c = None
loggedInUser = None  # track the current user's usr (id)

# taken from the week 6 lab sample code, connects to the database
def connect(path):
    global connection, c  # IMPORTANT: every function that uses sqlite3 should start with this line

    connection = sqlite3.connect(path)
    c = connection.cursor()
    c.execute('PRAGMA foreign_keys = ON;')  # enable foreign keys
    connection.commit()
    return 
    
# prompts user to log in, register, or exit program
def loginOrRegister():
    print('\nWelcome to Twitter (formerly X). Would you like to Sign In [sign in], Reigster [register], or Exit [exit]?')
    while(1):  
        openProgramChoice = input('> ').lower()
        if(openProgramChoice == 'sign in'):
            signIn()
            break
        elif(openProgramChoice == 'register'):
            register()
            break
        elif(openProgramChoice == 'exit'):
            print('exiting program...')
            sys.exit(0)
            break
        else:
            print('invalid input. Would you like to Sign In [sign in], Reigster [register], or Exit [exit]?')

    homeScreen()
    return

# gets user's id and password, authenticates it, and signs them in
def signIn():
    global connection, c, loggedInUser
    
    # enter and check username
    while(1):
        userID = input('Please enter your user ID: ')
        c.execute("SELECT * FROM users WHERE usr = ?;",(userID,))
        userInfo = c.fetchall()     
        if(userInfo):               # This checks if userInfo is not empty
            break                   # Valid user found, exit loop
        else:
            print('User ID not found.')
            
    # enter and check password
    while(1):
        #passID = input('Please enter your password (case-sensitive): ')
        passID = getpass.getpass(prompt='Please enter your password (case-sensitive): ', stream=None)
        c.execute("SELECT * FROM users WHERE usr = ? AND pwd = ?;", (userID, passID))
        userInfo = c.fetchall()
        if(userInfo):
            break
        else:
            print('Incorrect password.')
    loggedInUser = userID
    showFollowedTweets()
    
    return
          
# allows the user to input a name, email, and phone number. then the program makes a unique id and places them in the users database
def register():
    global connection, c, loggedInUser
    while(1):
        newUserName = input('Please enter your preferred name: ')
        if(newUserName != ''):
            break
        print("Name cannot be empty.")
    
    newUserEmail = None
    newUserPhoneNumber = None
    # get email
    while(1):
        newUserEmail = input('Please enter your email: ')
        
        # makes sure the email has a '@' and a '.'
        if('@' in newUserEmail and '.' in newUserEmail):
            periodPositions = [pos for pos, char in enumerate(newUserEmail) if char == '.']  # creates a list of all period indexes (so we can use the index of the last period)
            
            # makes sure the @ isnt the first character and the last period used isnt the last character, isnt before the @, and isnt the one right after the @ 
            # this removes the following invalid email formats: "@xxxx.com", "xxxx@.com", "xxxx.@com", "xxxx@com."
            if(newUserEmail.find('@') > 0 and periodPositions[-1] > newUserEmail.find('@')+1 and periodPositions[-1] < len(newUserEmail)-1):
                break
            else:
                print('Invalid email.')
        else:
            print('Invalid email.')
    
    # get phone number
    while(1):
        newUserPhoneNumber = input('Please enter your phone number: ')
        
        # makes sure the phone number is 10 digits
        if(len(newUserPhoneNumber) == 10):
            try:
                int(newUserPhoneNumber)
                break
            except:
                print('Phone number must be a number.')
            
        else:
            print('Invalid phone number.')
            
    # get password
    newUserPassword = input('Please enter a password (case-sensitive): ')
    
    # generate user id
    newUserID = 1
    unused = False
    c.execute("SELECT usr FROM users")
    usedIDs = c.fetchall()
    #print(usedIDs)
    
    # find first available id over the number 0
    while(not unused):
        unused = True
        for id in usedIDs:
            if(newUserID == id[0]):
                newUserID += 1
                unused = False
    
    # add to database
    c.execute("INSERT INTO users(usr,name,email,phone,pwd) VALUES (?,?,?,?,?);",(newUserID,newUserName,newUserEmail,newUserPhoneNumber,newUserPassword))
    print(f'Thank you for signing up! Your user ID is: {newUserID}.')
    connection.commit()
    loggedInUser = str(newUserID)
    return

# you get redirected here after logging in or registering
def homeScreen():
    global connection, c, loggedInUser
    c.execute("SELECT * FROM users WHERE usr = ?;", (loggedInUser,))   #Added a comma after loggedInUser to make it a single-value tuple.  # c.execute() expects the second parameter to be a tuple when using a single value
    currentUserInfo = c.fetchall()[0]  # the tuple of the logged in user's info
    
    print(f"\nWelcome to your home screen, {currentUserInfo[1]}!")
    currentUserID = currentUserInfo[0]
    # get user input and call associated functions
    while(1):
        showFollowedTweets()
        print(f"\nWelcome to your home screen, {currentUserInfo[1]}!")
        print("Options: see more tweets [more], search for tweets or users [search], compose a tweet [tweet], list followers [followers], logout [logout]")
        userInput = input("> ").lower()
        if userInput == 'more':
            showMoreTweetsInFeed()  # New function to handle pagination
            continue
        elif(userInput == 'search'):
            print('Would you like to search Tweets [tweets] or Users [users]?')
            while(1):
                searchMode = input("> ").lower()
                if(searchMode == 'tweets'):
                    searchTweets()
                    break
                elif(searchMode == 'users'):
                    searchUsers()
                    break
                else:
                    print('invalid search mode')
            break
        elif(userInput == 'tweet'):
            composeTweet()
            continue
        elif(userInput == 'followers'):
            listFollowers(currentUserID)
            continue
        elif(userInput == 'logout'):
            print('logging out...')
            loggedInUser = None
            loginOrRegister()
            return
        else:
            print('invalid option. ')
        
    return


####Raiyana####
def showMoreTweetsInFeed():
    global connection, c, loggedInUser
    
    query = ''' 
    SELECT DISTINCT t.tid,        -- Tweet ID
           t.writer_id,          -- ID of original tweet author
           u1.name,              -- Name of original tweet author
           t.text,               -- Content of the tweet
           t.tdate,              -- Date of original tweet
           t.ttime,              -- Time of original tweet
           r.retweeter_id,       -- ID of person who retweeted (NULL for direct tweets)
           u2.name,              -- Name of person who retweeted (NULL for direct tweets)
           r.rdate               -- Date of retweet (NULL for direct tweets)
    FROM tweets t
    JOIN users u1 ON t.writer_id = u1.usr
    LEFT JOIN retweets r ON t.tid = r.tid
    LEFT JOIN users u2 ON r.retweeter_id = u2.usr
    WHERE t.writer_id IN (SELECT flwee FROM follows WHERE flwer = ?)
       OR r.retweeter_id IN (SELECT flwee FROM follows WHERE flwer = ?)
    ORDER BY 
        CASE WHEN r.rdate IS NOT NULL THEN r.rdate ELSE t.tdate END DESC,
        t.ttime DESC
    LIMIT 5 OFFSET ?;
    '''
    
    startPosition = 5  # Start from the 6th tweet since the first 5 were shown
    while True:
        currentResults = c.execute(query, (loggedInUser, loggedInUser, startPosition)).fetchall()
        
        if not currentResults:
            print("No more tweets to show.")
            return
        
        # Display results
        print("\nMore tweets:")
        for i, (tid, writer_id, original_name, text, tweet_date, tweet_time,
               retweeter_id, retweeter_name, retweet_date) in enumerate(currentResults, startPosition + 1):
            print(f"\n{i}. Tweet ID: {tid}")
            if retweeter_id:
                print(f"   Originally by {original_name}")
                print(f"   Retweeted by {retweeter_name} on {retweet_date}")
            else:
                print(f"   By {original_name} on {tweet_date} at {tweet_time}")
            print(f"   {text}")
        
        # Show options
        print("\nOptions:")
        if len(currentResults) == 5:
            print("- Enter a number to select a tweet")
            print("- Type 'more' to see more tweets")
            print("- Type 'back' to return to menu")
        else:
            print("- Enter a number to select a tweet")
            print("- Type 'back' to return to menu")
        
        choice = input("> ").lower()
        
        if choice == 'more' and len(currentResults) == 5:
            startPosition += 5
            continue
        elif choice == 'back':
            return
        elif choice.isdigit():
            tweet_num = int(choice)
            if startPosition < tweet_num <= startPosition + len(currentResults):
                selected_tweet = currentResults[tweet_num - startPosition - 1]
                showTweetDetails(selected_tweet[0])  # Pass tweet ID
                continue
            else:
                print("Invalid tweet number.")
        else:
            print("Invalid choice.")




#####Raiyana#######
def showFollowedTweets():   
    global connection, c, loggedInUser
    
    query = ''' 
    SELECT DISTINCT t.tid,        -- Tweet ID
           t.writer_id,          -- ID of original tweet author
           u1.name,              -- Name of original tweet author
           t.text,               -- Content of the tweet
           t.tdate,              -- Date of original tweet
           t.ttime,              -- Time of original tweet
           r.retweeter_id,       -- ID of person who retweeted (NULL for direct tweets)
           u2.name,              -- Name of person who retweeted (NULL for direct tweets)
           r.rdate               -- Date of retweet (NULL for direct tweets)
    FROM tweets t
    JOIN users u1 ON t.writer_id = u1.usr
    LEFT JOIN retweets r ON t.tid = r.tid
    LEFT JOIN users u2 ON r.retweeter_id = u2.usr
    WHERE t.writer_id IN (SELECT flwee FROM follows WHERE flwer = ?)
       OR r.retweeter_id IN (SELECT flwee FROM follows WHERE flwer = ?)
    ORDER BY 
        CASE WHEN r.rdate IS NOT NULL THEN r.rdate ELSE t.tdate END DESC,
        t.ttime DESC;
    '''
    
    # Execute the query and handle results
    allResults = c.execute(query, (loggedInUser, loggedInUser)).fetchall()
    
    if not allResults:
        print("No tweets in your feed.")
        return
        
    # Display first 5 tweets
    print("\nYour feed:")
    for i, (tid, writer_id, original_name, text, tweet_date, tweet_time,
           retweeter_id, retweeter_name, retweet_date) in enumerate(allResults[:5], 1):
        print(f"\n{i}. Tweet ID: {tid}")
        if retweeter_id:
            print(f"   Originally by {original_name}")
            print(f"   Retweeted by {retweeter_name} on {retweet_date}")
        else:
            print(f"   By {original_name} on {tweet_date} at {tweet_time}")
        print(f"   {text}")
    
    if len(allResults) > 5:
        print("\nThere are more tweets available.")



 ####Raiyana####
def searchTweets(): 
    global connection, c, loggedInUser
    #the while loop Keeps prompting for new searches if no matches are founds
    while True:
        print("\nEnter keywords to search (separate multiple keywords with spaces):")
        print("Or type 'back' to return to home screen:")

        keywords_input = input("> ").strip()

        if keywords_input.lower() == 'back':
            homeScreen() # This will show the updated feed after the user returns from the search results
            
        keywords = keywords_input.split()
        if not keywords:
            print("No keywords entered.")
            continue
    
    
        allResults = []
        
        # Search for each keyword
        for keyword in keywords:
            if keyword.startswith('#'):
                # Hashtag search
                c.execute("""
                    SELECT DISTINCT t.tid, t.writer_id, u.name, t.text, t.tdate, t.ttime
                    FROM tweets t
                    JOIN users u 
                          ON t.writer_id = u.usr
                    JOIN hashtag_mentions hm 
                          ON t.tid = hm.tid
                    WHERE LOWER(hm.term) = LOWER(?)
                    ORDER BY t.tdate DESC, t.ttime DESC
                """, (keyword,))  # Use the full hashtag including #
            else:
                # Word search
                c.execute("""
                SELECT DISTINCT t.tid, t.writer_id, u.name, t.text, t.tdate, t.ttime
                FROM tweets t
                JOIN users u ON t.writer_id = u.usr
                LEFT JOIN hashtag_mentions hm ON t.tid = hm.tid
                WHERE (
                    (
                        t.text LIKE '% ' || ? || ' %' OR    -- matches word with spaces around it
                        t.text LIKE ? || ' %' OR            -- matches word at start
                        t.text LIKE '% ' || ? OR            -- matches word at end
                        t.text = ?                          -- matches exact text
                    ) AND LOWER(?) NOT LIKE '#%'
                )
                OR (LOWER(hm.term) = LOWER(?) AND LOWER(?) LIKE '#%')
            """, (
                    keyword, keyword, keyword, keyword, keyword,
                    keyword[1:] if keyword.startswith('#') else keyword, 
                    keyword
                    ))
                        # a tuple of parameters for the SQL query. 
            # if the keyword begins with a # (indicating it’s a hashtag). 
            # If so, it removes the # (keyword[1:]) so that it can match terms in the hashtag_mentions table.
            results = c.fetchall()   #fetches all the results from the query
            allResults.extend(results) #adds the results to the allResults list

        if not allResults:
            print("No tweets found matching your search.")
            continue
        
        # Remove duplicates and sort by date and time
        # Remove duplicates by using a set to track tweet IDs and only add unique ones
        uniqueResults = []
        seenTweetIds = set()

        for result in allResults:
            if result[0] not in seenTweetIds:
                uniqueResults.append(result)
                seenTweetIds.add(result[0])

        # Sort results by date and time in descending order
            uniqueResults.sort(key=lambda x: (x[4], x[5]), reverse=True) #sort the uniqueResults by the date (index 4) and time (index 5) fields, in descending order.

       
        startPosition = 0
        while True:     ## Inner loop for displaying results
            # Get current page of results
            currentResults = uniqueResults[startPosition:startPosition + 5]
            
            if not currentResults: #Checks if there are no results left to show.
                print("No more tweets to show.")
                break
                # startPosition = 0
                # continue
          

             # Display results
            print("\nMatching tweets:")
            for i, (tid, writer_id, writer_name, text, date, time) in enumerate(currentResults, 1):
                print(f"\n{i}. Tweet ID: {tid}")  # Added Tweet ID to display
                print(f"   By {writer_name} on {date} at {time}")
                print(f"   {text}")


        # Show options
            print("\nOptions:")
            if startPosition + 5 < len(uniqueResults):
                print("- Enter a number (1-5) to select a tweet")
                print("- Type 'more' to see more results")
                print("- Type 'back' to return to home screen")
            else:
                print("- Enter a number (1-5) to select a tweet")
                print("- Type 'back' to return to home screen")
        
            choice = input("> ").lower()
        
            if choice == 'more' and startPosition + 5 < len(uniqueResults):
                startPosition += 5
                continue
            elif choice == 'back':
                homeScreen()
            elif choice.isdigit() and 1 <= int(choice) <= len(currentResults):
                selected_tweet = currentResults[int(choice) - 1]
                showTweetDetails(selected_tweet[0])  # Pass tweet ID
                continue 
            else:
                print("Invalid choice.")
                continue

####Raiyana####
def showTweetDetails(tweet_id):  
    global connection, c, loggedInUser
    
    # Get tweet details
    tweet_query = """
    SELECT t.tid, t.writer_id, u.name, t.text, t.tdate, t.ttime,
           (SELECT COUNT(*) FROM tweets WHERE replyto_tid = t.tid) as reply_count,
           (SELECT COUNT(*) FROM retweets WHERE tid = t.tid) as retweet_count
    FROM tweets t
    JOIN users u ON t.writer_id = u.usr
    WHERE t.tid = ?
    """
    
    c.execute(tweet_query, (tweet_id,))
    tweetDetails = c.fetchone()
    
    if tweetDetails:
        tid, writer_id, name, text, date, time, replies, retweets = tweetDetails
        
        # Display tweet information
        print(f"\nTweet ID: {tid}")
        print(f"Tweet by {name} on {date} at {time}")
        print(f"Text: {text}")
        print(f"Replies: {replies}")
        print(f"Retweets: {retweets}")
        
        while True:  # Loop for user actions
            print("\nOptions:")
            print("1. Reply to this tweet (Type:'1')")
            print("2. Retweet this tweet (Type:'2')")
            print("3. Back to search results (Type:'3')")

            
            choice = input("> ")
            
            if choice == "1":
                composeTweet(replyTo=tid)  # Call composeTweet with the tweet ID
                continue
            elif choice == "2":
                retweet(tid)  # Call retweet with the tweet ID
                continue  # Go back to options after retweet
            elif choice == "3":
                return
            else:
                print("Invalid choice. Please try again.")


####Raiyana####
def retweet(tweet_id):  
    global connection, c, loggedInUser
    
    try:
        # Check if user has already retweeted this tweet
        c.execute("""
            SELECT COUNT(*) 
            FROM retweets 
            WHERE retweeter_id = ? AND tid = ?
        """, (loggedInUser, tweet_id))
        
        if c.fetchone()[0] > 0: #if the user has already retweeted the tweet, it prints a message and returns.
            # Update the spam flag to 1
            c.execute('''
                UPDATE retweets 
                SET spam = 1
                WHERE tid = ? AND retweeter_id = ?
            ''', (tweet_id, loggedInUser))
            connection.commit()
            print("You have already retweeted this tweet.")
            print("This tweet has been marked as spam because you tried to retweet it again.")
            return

        # Check for potential spam (3 or more retweets in a day)
        current_date = time.strftime("%Y-%m-%d")
        c.execute("""
            SELECT COUNT(*) 
            FROM retweets 
            WHERE retweeter_id = ? AND rdate = ?
        """, (loggedInUser, current_date))
        
        daily_retweets = c.fetchone()[0]
        is_spam = 1 if daily_retweets >= 2 else 0
        
        # Get the original tweet details
        c.execute("""
            SELECT t.text, u.name, t.writer_id
            FROM tweets t 
            JOIN users u ON t.writer_id = u.usr 
            WHERE t.tid = ?
        """, (tweet_id,))
        original_tweet = c.fetchone()
        original_writer_id = original_tweet[2]  # Get the writer_id
        
        # Insert the retweet with retweeter_id
        c.execute("""
            INSERT INTO retweets (retweeter_id, tid, writer_id, rdate, spam) 
            VALUES (?, ?, ?, ?, ?)
        """, (loggedInUser, tweet_id, original_writer_id, current_date, is_spam))
        
        connection.commit()
        
        print(f"You have retweeted: '{original_tweet[0]}' by {original_tweet[1]}")
        
        if is_spam:
            print("\nWARNING: This retweet has been marked as potential spam due to frequent retweeting.")
        
  
    except Exception as e:
        print(f"An error occurred: {e}")

       


########## Faiaz's Part #############

def searchUsers():
    global connection, c, loggedInUser
    print('Search Users')

    search_term = input("Enter a keyword to search for users: ").strip()
    page = 1  # Start at the first page
    per_page = 5  # Number of users to display per page

    while True:

        # Calculate offset for pagination
        offset = (page - 1) * per_page


        # SQL query to find matching users, sorted by name length
        query = """
            SELECT 
                u.usr, 
                u.name, 
                u.email, 
                LENGTH(u.name) AS name_length
            FROM 
                users u
            WHERE 
                LOWER(u.name) LIKE LOWER(?)
            ORDER BY 
                (u.name = ?) DESC, name_length ASC

            LIMIT ? OFFSET ?;
        """

        # Execute the query with parameters for exact match prioritization and pagination
        c.execute(query, (f"%{search_term}%", search_term, per_page, offset))

        results = c.fetchall()
        # print(results)

        if not results:
            print("No users found matching the search term.")
            searchUsers()
            return

        # Display the paginated search results
        print("\nMatching Users:")
        for i, user in enumerate(results):
            print(f"{i + 1}. ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

        # Option to select a user or load more results
        print("\nOptions:")
        print("1. Enter a number to select a user for more information.")
        if len(results) == per_page:
            print("2. Type 'next' to see more users.")
            print("3. Type 'exit' to return to the homescreen.")
        else:
            print("2. Type 'exit' to return to the homescreen.")  # Show as option 2 when "next" is not available
      
        choice = input("Choose an option: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(results):
            # Show more information about the selected user
            selected_user = results[int(choice) - 1]
            showUserDetails(selected_user[0])  # Pass the selected user's ID
            
        elif choice.lower() == 'next' and len(results) == per_page:
            page += 1
        elif choice.lower() == 'exit':
            homeScreen()
            break
        else:
            print("Invalid option. Please try again.")

    return

def showUserDetails(user_id):
    global connection, c, loggedInUser

    # Query to get the selected user's details
    details_query = """
        SELECT 
            u.name, 
            (SELECT COUNT(*) FROM tweets WHERE writer_id = u.usr) AS tweet_count,
            (SELECT COUNT(*) FROM follows WHERE flwer = u.usr) AS following_count,
            (SELECT COUNT(*) FROM follows WHERE flwee = u.usr) AS followers_count
        FROM 
            users u
        WHERE 
            u.usr = ?;
    """

    # Query to get the selected user's 3 most recent tweets
    tweets_query = """
        SELECT 
            text, tdate, ttime 
        FROM 
            tweets 
        WHERE 
            writer_id = ?
        ORDER BY 
            tdate DESC, ttime DESC
        LIMIT 3;
    """

    # Execute the details query
    c.execute(details_query, (user_id,))
    user_details = c.fetchone()

    if user_details:
        print(f"\nUser: {user_details[0]}")
        print(f"Number of Tweets: {user_details[1]}")
        print(f"Following: {user_details[2]}")
        print(f"Followers: {user_details[3]}")

        # Execute the recent tweets query
        c.execute(tweets_query, (user_id,))
        recent_tweets = c.fetchall()

        print("\nRecent Tweets:")
        for tweet in recent_tweets:
            print(f"- {tweet[0]} (Date: {tweet[1]}, Time: {tweet[2]})")

        # Option to follow the user or see more tweets
        print("\nOptions:")
        print("1. Type 'follow' to follow this user.")
        print("2. Type 'more' to see more tweets.")
        print("3. Type 'back' to return to search results.")

        choice = input("Choose an option: ").strip().lower()

        if choice == 'follow':
            followUser(loggedInUser, user_id)
        elif choice == 'more':
            showMoreTweets(user_id)
        elif choice == 'back':
            return
        else:
            print("Invalid option.")

    else:
        print("User not found.")

def listFollowers(user_id):
    global connection, c, loggedInUser
    print("\nList Followers")

    page = 1  # Start at the first page
    per_page = 5  # Number of followers to display per page

    while True:
        # Calculate offset for pagination
        offset = (page - 1) * per_page

        # SQL query to fetch followers of the logged-in user with pagination
        followers_query = """
            SELECT 
                u.usr, 
                u.name, 
                u.email
            FROM 
                follows f
            JOIN 
                users u ON f.flwer = u.usr
            WHERE 
                f.flwee = ?
            LIMIT ? OFFSET ?;
        """

        # Execute the query with pagination parameters
        c.execute(followers_query, (loggedInUser, per_page, offset))
        followers = c.fetchall()

        if not followers:
            print("No more followers to display.")
            break

        # Display the paginated followers
        print("\nYour Followers:")
        for i, follower in enumerate(followers):
            print(f"{i + 1}. ID: {follower[0]}, Name: {follower[1]}, Email: {follower[2]}")

        # Options to select a follower, see more results, or exit
        print("\nOptions:")
        print("1. Enter a number to select a follower and view more information.")
        if len(followers) == per_page:
            print("2. Type 'next' to see more followers.")
        print("3. Type 'exit' to return to the main menu.")

        choice = input("Choose an option: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(followers):
            # Show more information about the selected follower
            selected_follower = followers[int(choice) - 1]
            showUserDetails(selected_follower[0])  # Pass the selected follower's ID
        elif choice.lower() == 'next' and len(followers) == per_page:
            page += 1
        elif choice.lower() == 'exit':
            break
        else:
            print("Invalid option. Please try again.")

    return

def followUser(follower_id, followee_id):
    global connection, c

    # Check if the user is trying to follow themselves
    #Since loggedInUser is stored as a string and the IDs from the database are integers
    #we convert both to strings for comparison
    if str(follower_id) == str(followee_id):  
        print()
        print("You cannot follow yourself!")
        print()
        return
    
    try:
        # Insert the follow record
        follow_query = """
            INSERT INTO follows (flwer, flwee, start_date)
            VALUES (?, ?, DATE('now'));
        """
        c.execute(follow_query, (follower_id, followee_id))
        connection.commit()
        print()
        print("You are now following this user!")
        print()
    except sqlite3.IntegrityError:
        print()
        print("You are already following this user!")
        print()

def showMoreTweets(user_id):
    global connection, c

    # Query to fetch more tweets beyond the initial 3
    tweets_query = """
        SELECT 
            text, tdate, ttime 
        FROM 
            tweets 
        WHERE 
            writer_id = ?
        ORDER BY 
            tdate DESC, ttime DESC
        LIMIT 10 OFFSET 3;  -- Starts from the 4th tweet

    """

    c.execute(tweets_query, (user_id,))
    more_tweets = c.fetchall()

    # Check if there are additional tweets
    if more_tweets:
        print("\nMore Tweets:")
        for tweet in more_tweets:
            print(f"- {tweet[0]} (Date: {tweet[1]}, Time: {tweet[2]})")
        print()
    else:
        print("\nNo additional tweets to display.")

###########################################

def composeTweet(replyTo = None):  ##Utsha##
    global connection, c, loggedInUser

    print("Enter your tweet. Do no repeat hashtags.")
    invalidTweet = True
    tweet = ""
    hashtags = []

    while invalidTweet:
        tweet = input("> ")
 
        if tweet.strip() == "":
            print("Invalid tweet. Tweet cannot be empty")
        elif '#' in tweet:
            wordsList = tweet.split()
            hashtags = [word for word in wordsList if word.startswith("#") and word[1:] != ""]
            repeatedHashtag = checkRepeatedHashtags(hashtags)

            if repeatedHashtag:
                print("Invalid tweet. Tweet cannot repeat hashtag")
            else:
                invalidTweet = False
        else:
            invalidTweet = False

    #Edited by Raiyana
    # Determine the next available tid
    #query selects all tid values from the tweets table and orders them in ascending order.
    c.execute("""
               SELECT tid 
               FROM tweets 
               ORDER BY tid ASC
               """)
    #result is stored in existing_tids, which is a list of tuples, each containing a single tid.
    existing_tids = c.fetchall()
    
    next_tid = 1
    # iterates over each tid in existing_tids.
    for (tid,) in existing_tids:
        if tid == next_tid:  #means this ID is already taken, so next_tid is incremented by 1 to check the next number.
            next_tid += 1
        else:
            break   #if the current tid is not equal to next_tid, it breaks out of the loop.



    currentDate = time.strftime("%Y-%m-%d")
    currentTime = time.strftime("%H:%M:%S")

    c.execute("INSERT INTO tweets VALUES (?,?,?,?,?,?);", (next_tid, loggedInUser, tweet, currentDate, currentTime, replyTo))
    if (hashtags != []):
        for tag in hashtags:
            c.execute("INSERT INTO hashtag_mentions VALUES (?,?);", (next_tid, tag))

    print(f"Tweeted successfully: {tweet}")
    connection.commit()




def checkRepeatedHashtags(tagList):  #Utsha
    tagSet = set()
    for tag in tagList:
        if tag.lower() in tagSet:
            return True
        else:
            tagSet.add(tag)
    return False



def main():
    global connection, c
    if(len(sys.argv) != 2):
        print("Please enter the desired database file path when starting the program. Exiting...")
        sys.exit(0)
    path = sys.argv[1]  # takes file name from command line arguments
    #path = './prj-sample.db'  # use this if you dont wanna pass something through each time you run the program. otherwise, comment it out pls!
    connect(path)
    # makes sure the table works by trying a query
    try:
        c.execute("SELECT * FROM users WHERE usr = -1;")
    except:
        print('Invalid table. Exiting...')
        sys.exit(0)
        
    loginOrRegister()
    

if __name__ == '__main__':
    main()