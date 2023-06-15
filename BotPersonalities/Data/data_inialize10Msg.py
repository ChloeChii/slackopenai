import os
import sqlite3

# use gensim and nltk for training model
import gensim
import nltk
from dotenv import load_dotenv
from gensim import corpora
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

app = App(token=os.environ['SLACK_APP_TOKEN']) # Use the environment variable
client = WebClient(token=os.environ['SLACK_BOT_TOKEN']) # Use the environment variable
channel_id = os.environ['CHANNEL_ID'] # Use the environment variable

try:
    conversation_history = client.conversations_history(channel=channel_id)
    messages = conversation_history['messages']
except SlackApiError as e:
    print("Error fetching conversation history: {}".format(e))

conn = sqlite3.connect(os.getenv("DB_NAME"))
c = conn.cursor()

# add a count to store oonly the 10 most recent messages
counter = 0

for message in messages:
    content = message['text']
    ts = message['ts']
 
    # convert role to user or assistant
    if "bot_id" in message:
        role = "assistant"
    else:
        role = "user"

    # insert the new message into DB if it was created by user
    c.execute("INSERT INTO messages VALUES (?, ?, ?)", (ts, role, content))

    if 'thread_ts' in message:
        try:
            replies = client.conversations_replies(
                channel=channel_id,
                ts=ts
            )
            for reply in replies['messages']:
                # skip the first one message which is the main message
                reply_role = reply['user']
                reply_content = reply['text']
                thread_ts = reply['ts']

                c.execute("SELECT * FROM messages WHERE ts = ?", (thread_ts,))
                result = c.fetchone()

                if result is None:
                    c.execute("INSERT INTO messages VALUES (?, ?, ?)", (thread_ts, reply_role, reply_content))
        except SlackApiError as e:
            print("Error fetching replies for message {}: {}".format(message['thread_ts'], e))
    counter += 1
    if counter >= 10:
        break
conn.commit()
conn.close()