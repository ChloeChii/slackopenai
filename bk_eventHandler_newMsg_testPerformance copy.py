import os
import sqlite3
import time

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
model = os.environ['MODEL']

@app.event("message")
def handle_message(event, say, body):
    # the bot get the message
    text = event["text"]
    role = event["user"]
    ts = event["ts"]
        
    # assign user role
    if "bot_id" in event:
        role = "assistant"
    else:
        role = "user"
    
    conn = sqlite3.connect(os.getenv("DB_NAME"))
    c = conn.cursor()

    #insert the msg into DB
    if text.lower().startswith("assistant:"):
        text = text.split(" ", 1)[1]
    if text.lower().startswith("answer:"):
        text = text.split(" ", 1)[1]

    # drop the oldest message
    current_timestamp = int(time.time())
    print("Start timestamp:", current_timestamp)

    # insert the latest one message
    c.execute("INSERT INTO messages VALUES (?, ?, ?)", (ts, role, text))
    conn.commit()
    

    if "bot_id" not in event:
        # retrieve the 9 most recent messages from DB
        c.execute("SELECT * FROM messages ORDER BY ts DESC LIMIT 9")
        rows = c.fetchall()
        current_timestamp = int(time.time())
        print("End timestamp:", current_timestamp)
        # Create the new message dictionary
        new_message = {'system', '1681962590.1', 'You are a creative assistant that gives long answers.'}
        # Append the new message to the end of the list
        rows.append(new_message)
        rows = rows[::-1]
        print(rows)

        #  Combine the messages into a list of dictionaries
        messages = []
        for row in rows:
            print(row)
            message = {"role": list(row)[1], "content": list(row)[2]}
            messages.append(message)
        
        try:
        # Generate a response using OpenAI's gpt-3.5-turbo language model
            openai.api_key = os.environ['OPENAI_API_KEY']
            # multithread, race conditoon of monitor, 
            # write the response to file

            # change Completion to ChatCompletion
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages
            )
            # Extract the generated text from the response
            generated_text = response['choices'][0]['message']['content']
            length = len(generated_text)

            # name the file with an increasing counter
            
            
            if length != 0:
                # Post the generated text as a message in Slack
                if generated_text.lower().startswith("assistant:") or generated_text.lower().startswith("answer:"):
                    generated_text = generated_text.split(" ", 1)[1]

                counter=1
                filename = f'example_{counter}.txt'
                with open(filename, 'w') as file:
                    file.write(message)
                    file.write('\n')
                    file.write(generated_text)
                count += 1


                client.chat_postMessage(channel=channel_id, text=generated_text)
        except SlackApiError as e:
            print("Error posting message: {}".format(e))
    
        # close the db connection
        conn.close()

if __name__ == "__main__":
    SocketModeHandler(app, app_token=os.getenv("SLACK_APP_TOKEN")).start()
