-- Insert test users
INSERT INTO users (usr, name, email, phone, pwd) VALUES 
(14, 'John', 'john4@email.com', '1234567896', 'pass123'),
(15, 'John Doe', 'jdoe2@email.com', '2345678902', 'pass456'),
(16, 'Bob John', 'bobjohn@email.com', '3456789013', 'pass789'),
(17, 'Alice crown', 'alicecrown@email.com', '4567890125', 'pass012'),
(18, 'Charlie puth', 'charlieputh@email.com', '5678901235', 'pass345'),
(19, 'David puth', 'davidputh@email.com', '6789012343', 'pass678'),
(20, 'Eva johnson', 'evaj@email.com', '7890123452', 'pass901'),
(21, 'Frank Johnson', 'frank4@email.com', '8901234564', 'pass234');


.schema tweets


INSERT INTO tweets (tid, writer_id, text, tdate, ttime, replyto_tid) VALUES 
(1007, 20, 'This is a sample tweet', date('now'), time('now'), NULL),
(1008, 21,'Another sample tweet', date('now'), time('now'), NULL),
(1009, 22, 'A reply to tweet 1007', date('now'), time('now'), 1007);




DELETE FROM follows WHERE flwer = '1';
DELETE FROM tweets WHERE writer_id IN ('2', '3');
DELETE FROM tweets WHERE tid IN (1, 2);  -- Specify the tweet IDs we'll use
DELETE FROM retweets WHERE tid IN (1, 2);  -- Same tweet IDs as above
-- Insert test users and relationships
INSERT INTO follows (flwer, flwee, start_date) VALUES 
('1', '4', DATE('now')); -- You follow user1

-- Insert test tweets
INSERT INTO tweets (tid, writer_id, text, tdate, ttime) VALUES 
(97, '4', 'Original tweet from followed user', DATE('now'), TIME('now')),
(98, '5', 'Tweet from unfollowed user', DATE('now'), TIME('now'));

-- Insert test retweets
INSERT INTO retweets (retweeter_id, tid, writer_id, rdate, spam) VALUES 
('5', 97, '4', DATE('now'), 0),  -- Unfollowed user retweets followed user's tweet
('4', 98, '5', DATE('now'), 0);  -- Followed user retweets unfollowed user's tweet



SELECT * FROM tweets WHERE tid = 99;
SELECT * FROM retweets WHERE tid = 99;

-- Check if Emma's user ID matches
SELECT usr, name FROM users WHERE name = 'Emma';




SELECT * FROM follows WHERE flwer = 3 AND flwee = 1;

-- Then unfollow
DELETE FROM follows WHERE flwer = 3 AND flwee = 1;














INSERT INTO tweets (tid, writer_id, text, tdate, ttime) VALUES
(131, 1, 'First day at my new job! #excited', '2024-03-15', '09:00:00'),
(102, 1, 'Just had the best coffee ever #coffee', '2024-03-15', '10:30:00'),
(103, 1, 'Working on a new project #coding', '2024-03-15', '14:15:00'),
(104, 1, 'Lunch break with colleagues #worklife', '2024-03-15', '12:00:00'),
(105, 1, 'Made significant progress today!', '2024-03-14', '16:45:00'),
(106, 1, 'Morning workout complete #fitness', '2024-03-14', '07:30:00'),
(107, 1, 'Team meeting went great #work', '2024-03-14', '11:00:00'),
(108, 1, 'Learning new technologies #tech', '2024-03-14', '15:20:00'),
(109, 1, 'Weekend plans: coding marathon', '2024-03-13', '18:00:00'),
(110, 1, 'Just solved a tough bug #debugging', '2024-03-13', '14:30:00'),
(111, 1, 'Reading a great book on AI #learning', '2024-03-13', '20:00:00'),
(112, 1, 'Early morning thoughts #productive', '2024-03-13', '06:45:00'),
(113, 1, 'Beautiful sunset today! #nature', '2024-03-12', '17:30:00'),
(114, 1, 'Started a new side project #coding', '2024-03-12', '13:15:00'),
(115, 1, 'Great team collaboration today', '2024-03-12', '15:45:00'),
(116, 1, 'Morning run was refreshing #health', '2024-03-12', '08:00:00'),
(117, 1, 'Learning about databases #SQL', '2024-03-11', '11:30:00'),
(118, 1, 'Code review session was helpful', '2024-03-11', '14:00:00'),
(119, 1, 'Working from home today #remote', '2024-03-11', '09:15:00'),
(120, 1, 'Evening walk with music #peace', '2024-03-11', '18:30:00'),
(121, 1, 'Brainstorming new ideas #creative', '2024-03-10', '10:45:00'),
(122, 1, 'Project deadline met! #success', '2024-03-10', '16:00:00'),
(123, 1, 'Coffee and code #developer', '2024-03-10', '08:30:00'),
(124, 1, 'Team lunch was fun #colleagues', '2024-03-10', '13:00:00'),
(125, 1, 'Learning Python tricks #python', '2024-03-09', '15:30:00'),
(126, 1, 'Morning meditation #mindfulness', '2024-03-09', '07:00:00'),
(127, 1, 'Code optimization complete', '2024-03-09', '11:45:00'),
(128, 1, 'Weekend coding session #focus', '2024-03-09', '14:30:00'),
(129, 1, 'New feature deployed #dev', '2024-03-08', '16:15:00'),
(130, 1, 'Starting the day with goals #motivation', '2024-03-08', '08:45:00');

-- Insert corresponding hashtag mentions
INSERT INTO hashtag_mentions (tid, term) VALUES
(131, '#excited'),
(102, '#coffee'),
(103, '#coding'),
(104, '#worklife'),
(106, '#fitness'),
(107, '#work'),
(108, '#tech'),
(110, '#debugging'),
(111, '#learning'),-
(112, '#productive'),
(113, '#nature'),
(114, '#coding'),
(116, '#health'),
(117, '#SQL'),
(119, '#remote'),
(120, '#peace'),
(121, '#creative'),
(122, '#success'),
(123, '#developer'),
(124, '#colleagues'),
(125, '#python'),
(126, '#mindfulness'),
(128, '#focus'),
(129, '#dev'),
(130, '#motivation');





INSERT INTO tweets (tid, writer_id, text, tdate, ttime) VALUES
    (102, 1, 'Just had the best coffee ever #coffee', '2024-03-15', '10:30:00'),
    (103, 1, 'Working on a new project #coding', '2024-03-15', '14:15:00'),
    (104, 1, 'Lunch break with colleagues #worklife', '2024-03-15', '12:00:00'),
    (105, 1, 'Made significant progress today!', '2024-03-14', '16:45:00'),
    (106, 1, 'Morning workout complete #fitness', '2024-03-14', '07:30:00'),
    (107, 1, 'Team meeting went great #work', '2024-03-14', '11:00:00'),
    (108, 1, 'Learning new technologies #tech', '2024-03-14', '15:20:00'),
    (109, 1, 'Weekend plans: coding marathon', '2024-03-13', '18:00:00'),
    (110, 1, 'Just solved a tough bug #debugging', '2024-03-13', '14:30:00'),
    (111, 1, 'Reading a great book on AI #learning', '2024-03-13', '20:00:00'),
    (112, 1, 'Early morning thoughts #productive', '2024-03-13', '06:45:00'),
    (113, 1, 'Beautiful sunset today! #nature', '2024-03-12', '17:30:00'),
    (114, 1, 'Started a new side project #coding', '2024-03-12', '13:15:00'),
    (115, 1, 'Great team collaboration today', '2024-03-12', '15:45:00'),
    (116, 1, 'Morning run was refreshing #health', '2024-03-12', '08:00:00'),
    (117, 1, 'Learning about databases #SQL', '2024-03-11', '11:30:00'),
    (118, 1, 'Code review session was helpful', '2024-03-11', '14:00:00'),
    (119, 1, 'Working from home today #remote', '2024-03-11', '09:15:00'),
    (120, 1, 'Evening walk with music #peace', '2024-03-11', '18:30:00'),
    (121, 1, 'Brainstorming new ideas #creative', '2024-03-10', '10:45:00'),
    (122, 1, 'Project deadline met! #success', '2024-03-10', '16:00:00'),
    (123, 1, 'Coffee and code #developer', '2024-03-10', '08:30:00'),
    (124, 1, 'Team lunch was fun #colleagues', '2024-03-10', '13:00:00'),
    (125, 1, 'Learning Python tricks #python', '2024-03-09', '15:30:00'),
    (126, 1, 'Morning meditation #mindfulness', '2024-03-09', '07:00:00'),
    (127, 1, 'Code optimization complete', '2024-03-09', '11:45:00'),
    (128, 1, 'Weekend coding session #focus', '2024-03-09', '14:30:00'),
    (129, 1, 'New feature deployed #dev', '2024-03-08', '16:15:00'),
    (130, 1, 'Starting the day with goals #motivation', '2024-03-08', '08:45:00');
    