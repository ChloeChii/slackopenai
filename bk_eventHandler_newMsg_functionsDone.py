import os
import sqlite3

import openai
from dotenv import load_dotenv
from slack import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

# load the .env file
load_dotenv()

# Event API & Web API
app = App(token=os.environ['SLACK_APP_TOKEN']) # Use the environment variable
client = WebClient(token=os.environ['SLACK_BOT_TOKEN']) # Use the environment variable
channel_id = os.environ['CHANNEL_ID'] # Use the environment variable


@app.event("message")
def handle_message(event, say, body):
    # the bot get the message
    text = event["text"]
    role = event["user"]
    ts = event["ts"]
        
        
    if "bot_id" in event:
        role = "assistant"
    else:
        role = "user"
    
    conn = sqlite3.connect(os.getenv("DB_NAME"))
    c = conn.cursor()

    #insert the msg into DB
    print("insert the msg to DB")
    if text.lower().startswith("assistant:"):
        text = text.split(" ", 1)[1]
    # drop the oldest message
    c.execute("DELETE FROM messages WHERE ts IN (SELECT ts FROM messages ORDER BY ts ASC LIMIT 1)")
    c.execute("INSERT INTO messages VALUES (?, ?, ?)", (ts, role, text))
    conn.commit()

    if "bot_id" not in event:
        
        # retrieve the 10 most recent messages from DB
        c.execute("SELECT * FROM messages ORDER BY ts DESC")
        rows = c.fetchall()
        rows = rows[::-1]

        #  Combine the messages into a list of dictionaries
        messages = []
        for row in rows:
            message = {"role": row[1], "text": row[2]}
            print(row[1])
            messages.append(message)
        
        print(messages)


        try:
        # Generate a response using OpenAI's GPT-3 language model
            openai.api_key = os.environ['OPENAI_API_KEY']
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="\n".join([f"{message['role']}: {message['text']}" for message in messages]),
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            # Extract the generated text from the response
            generated_text = response.choices[0].text.strip()
            length = len(generated_text)
            
            if length != 0:
                print("generated text length")
                print(length)
                print(generated_text)
                # Post the generated text as a message in Slack
                if generated_text.lower().startswith("assistant:"):
                    generated_text = generated_text.split(" ", 1)[1]
                client.chat_postMessage(channel=channel_id, text=generated_text)
        except SlackApiError as e:
            print("Error posting message: {}".format(e))
    
        # close the db connection
        conn.close()

if __name__ == "__main__":
    SocketModeHandler(app, app_token=os.getenv("SLACK_APP_TOKEN")).start()
