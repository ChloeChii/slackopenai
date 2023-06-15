import json
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
    # print("handle")
    # the bot get the message
    text = event["text"]
    role = event["user"]
    ts = event["ts"]
    
    # assign user role
    if "bot_id" in event:
        role = "assistant"
    else:
        role = "user"
    
    if "bot_id" not in event:
        
        #  Combine the messages into a list of dictionaries
        messages = []
        message = {"role": role, "content": text}
        messages.append(message)
        with open('prompts_long_description.txt', 'r') as file:
            # Read the file content
            for line in file:
                # Extract the personality from each line (assuming each line is a personality)
                personality = line.strip()
                print(personality)
                # Extract the value of the 'personality' variable
                message = {"role": "system", "content": personality}
                messages.append(message)
                time.sleep(60)

                try:
                # Generate a response using OpenAI's gpt-3.5-turbo language model
                    openai.api_key = os.environ['OPENAI_API_KEY']

                    # change Completion to ChatCompletion
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=messages
                    )
                    
                    filename = f'example_{text}.txt'
                    with open(filename, 'w') as file:
                        my_str = json.dumps(message)
                        file.write(my_str)
                        file.write('\n')
                        res = json.dumps(response)
                        file.write(res)
                    # Extract the generated text from the response
                    generated_text = response['choices'][0]['message']['content']
                    length = len(generated_text)

                    # name the file with an increasing counter
                    comment = "I'm a bot who is " +personality
                    client.chat_postMessage(channel=channel_id, text = comment)
                    if length != 0:
                        # Post the generated text as a message in Slack
                        if generated_text.lower().startswith("assistant:") or generated_text.lower().startswith("answer:"):
                            generated_text = generated_text.split(" ", 1)[1]

                        client.chat_postMessage(channel=channel_id, text=generated_text)
                except SlackApiError as e:
                    print("Error posting message: {}".format(e))
    
if __name__ == "__main__":
    SocketModeHandler(app, app_token=os.getenv("SLACK_APP_TOKEN")).start()
