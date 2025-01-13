# Twitter-like application using Python and SQLite

This project was developed in collaboration with:
- Utsha Samanta
- Faiaz Bin Nesar
- Raiyana Rahman
- Sydney Smythe


## Group work break-down strategy
Work done by each member (along with a time estimate)

Sydney (time estimate: 8 hours): 
- Created and set up the python file with SQL communication
- Handled command-line arguments and command-line argument / database validation
- Created the initial sign-in / register / exit screen
- Programmed the sign-in and register functions, along with input validation and unique user ID assignment
- Created the home screen command loop

Utsha (time estimate: 7 hours):
- Created the ability for users to post new tweets
- Created the ability to reply to a tweet
- Created the system to detect and store hashtags in tweets
- Tested the code thoroughly and caught multiple bugs

Raiyana (time estimate: 15 hours):
- Created the newsfeed
- Created pagination code for Newsfeed 
- Created the system to search for tweets with multiple keywords and hashtags
- Added pagination for search results
- Implemented detailed view of tweets
- Added reply and retweet options
- Displayed tweet metadata (date, time, replies, retweets)
- Created retweet functionality
- Created the system to set spam flags for duplicate retweets
- Managed database operations for retweets
- Implemented tweet ID generation logic in the composeTweet()
- Implemented navigation between different screens
- Handled error cases and edge conditions
  

Faiaz (time estimate: 8 hours):
- Created the system to search for users and view extra stats of the users
- Created the list followers functionality where the user can see the stats of the followers and follow them back
- Created the pagination code used throughout the project
- Created the system to follow users

## Method of coordination
To coordinate our work, we used a combination of GitHub, Instagram, and Google Docs. We used GitHub as a place to keep our code, which we kept in separate branches while being worked on. The code was then merged into the main branch after our part was completed. We used Instagram to communicate throughout the project, notifying other members of bugs found in the code, checking for progress updates, and discussing testing methods. Our Google Doc was used to outline the work each of us needed to do.


# Code execution guide
1. Clone the repository
2. Navigate to the project directory
3. Call the Python file in the linux command line as follows: python3 system.py &lt;PATH-OF-DATABASE&gt;
 


## More detail of any AI tool used.
### Claude 3.5 Sonnet (Anthropic)
Used primarily for debugging assistance and code review:

1. Debugging Support
   - Helped identify syntax errors in SQL queries
   - Assisted with pagination-related bugs
   - Suggested fixes for database connection issues

2. Code Review
   - Suggested potential edge cases for testing
   - Pointed out possible security considerations
   - Helped identify redundant code

### How AI Was Used Responsibly
1. AI was used only for debugging and review purposes
2. All suggestions were thoroughly reviewed before implementation
3. Core functionality was designed and implemented by team members
4. AI was not used for direct code generation
5. All critical decisions were made by the team
 
### Limitations and Human Oversight
1. All database schema decisions were made by the team
2. Core application logic was designed by team members
3. AI suggestions were used as guidance, not direct implementation
4. Final code review and testing were performed by team members

