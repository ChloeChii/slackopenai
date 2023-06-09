import os
import sqlite3

import openai
from dotenv import load_dotenv
from slack import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import SlackApiError

# load the .env file
load_dotenv()

# Event API & Web API
app = App(token=os.environ['SLACK_APP_TOKEN']) # Use the environment variable
client = WebClient(token=os.environ['SLACK_BOT_TOKEN']) # Use the environment variable
channel_id = os.environ['CHANNEL_ID'] # Use the environment variable

# This is the original version for chatgnt togets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # the bot get the message
    text = body["text"]
    # channel_id = event["channel"]
    role = body["user"]
    ts = body["ts"]
    
    if "bot_id" not in body:
        # connect to DB
        print("connect to SQlite")
        conn = sqlite3.connect(os.getenv("DB_NAME"))
        c = conn.cursor()

        #insert the msg into DB
        print("insert the msg to DB")
        c.execute("INSERT INTO messages VALUES (?, ?, ?)", (ts, role, text))
        conn.commit()
        

        # retrieve the 10 most recent messages from DB
        c.execute("SELECT * FROM messages ORDER BY ts DESC LIMIT 10")
        messages = c.fetchall()
        messages = messages[::-1]

        #  Combine the message into a single prompt
        print("Combine the messages into a single prompt")
        prompt = "\n".join([message[2] for message in messages])
        print(prompt)

        try:
        # Generate a response using OpenAI's GPT-3 language model
            # print("generating response")
            # openai.api_key = OPENAI_API_KEY
            openai.api_key = os.environ['OPENAI_API_KEY']
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            # Extract the generated text from the response
            generated_text = response.choices[0].text.strip()
            # print("generated_text")
            length = len(generated_text)
            print("generated text length")
            print(length)
            if length != 0:
            # Post the generated text as a message in Slack
                client.chat_postMessage(channel=channel_id, text=generated_text)
        except SlackApiError as e:
            print("Error posting message: {}".format(e))
    
        # close the db connection
        conn.close()


if __name__ == "__main__":
    SocketModeHandler(app, app_token=os.getenv("SLACK_APP_TOKEN")).start()

    