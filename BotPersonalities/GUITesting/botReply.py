import json
import os
import time

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes
load_dotenv()
model = os.environ['MODEL']

@app.route('/generate_response', methods=['POST'])
def generate_response():
    # Retrieve the user question from the request
    data = request.get_json()
    question = data.get('question')
    systemMessages = data.get('systemMessages')

    print("Received question:", question)
    print("Received systemMessages:", systemMessages)

    messages = []
    message = {"role": 'user', "content": question}
    messages.append(message)
    message = {"role": 'system', "content": systemMessages}


    # Generate a response using OpenAI's gpt-3.5-turbo language model
    openai.api_key = os.environ['OPENAI_API_KEY']

    # change Completion to ChatCompletion
    openairesponse = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    
    # Extract the generated text from the response
    generated_text = openairesponse['choices'][0]['message']['content']

    # name the file with an increasing counter
    # comment = "I'm a bot who is " + systemMessages
        
        # Generate the response based on the question (replace this with your logic)
    response = generated_text
    # response =  systemMessages

    # Return the response as a JSON object
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)