
Step 1:
## Create the database in Slack using sqlite3
Date:2023/4/12
Command: python data_createDB.py
How it runs: This code uses SQlite3 as database and creates a table schema with two columns, role column and context column using c.execute function with SQL command. The role can be "system", "user", and "assistant", and the content is the message that was sent by them on slack. After finishing runing the code, the code will generate a slack_messages.db file in the same directory. 
The schema of the database is (ts timestamp primary key, role text, content text)
Note that you will need to replace <SLACK_BOT_TOKEN> and <channel_id> with your own values and ensure that your Slack app has the appropriate permissions to access SQlite3

Step 2:
## Initialize data 
Date: 2023/4/12
Command: python data_initializeMsg.py
How it runs: This code uses "client.conversations_history" to loop through all the messages identified by "ts" and insert the replies into DB. If the message has replies, the code will iterate through all of the replies in the thread by thread_ts, and insert the replies into DB. After inserting the records into DB, the code will generate a new file in the same directory named slack_message.db
Note that you may need to install the SQLite viewer extension to open the .db file

Step 3:
## Enables the bot to retrieve 10 most recent message

Date: 2023/3/29
Command: python eventHandler_newMsg.py
How it runs: This code used an annotation to handle the "app_mention " event, insert the new message created by user into DB and then retrive the most 10 recent messages by timestamp, composed the history message as prompt and send the prompt to ChatGBT API. Then the code used openai.Completion.create to create responsed to the message.








