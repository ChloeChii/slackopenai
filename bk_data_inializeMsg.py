import os
import sqlite3

# use gensim and nltk for training model
import gensim
import nltk
from gensim import corpora
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = App(token=os.environ['SLACK_APP_TOKEN']) # Use the environment variable
client = WebClient(token=os.environ['SLACK_BOT_TOKEN']) # Use the environment variable
channel_id = os.environ['CHANNEL_ID'] # Use the environment variable


# Download the NLTK tokenizer data
nltk.download('punkt')  

try:
    conversation_history = client.conversations_history(channel=channel_id)
    messages = conversation_history['messages']
except SlackApiError as e:
    print("Error fetching conversation history: {}".format(e))

conn = sqlite3.connect(os.getenv("DB_NAME"))
c = conn.cursor()
overallContent = ""

for message in messages:
    # role = message['user'] 
    content = message['text']
    ts = message['ts']
    
    # overallContent += message['text']
    # overallContent += ","
    # print(overallContent)
    # print("overallContent")

    ### Add below to achieve the tag function
    # In the above code, I defined a list of documents to extract topics from, 
    # and used the gensim library to tokenize the documents, create a bag-of-words 
    # representation of the documents, and train an LDA topic model on the bag-of-words 
    # corpus. I then used the trained LDA model to extract the top topic for each document.
    # Note that this is just an example implementation, and you may need to adjust the parameters of the topic model or use a different topic model depending on your specific use case.
    tokenized_documents = [doc.lower().split(",") for doc in content]
    # print("tokenized_documents")

    # print(tokenized_documents)
    # # Create a dictionary from the tokenized documents
    dictionary = corpora.Dictionary(tokenized_documents)
    # # Create a bag-of-words representation of the documents
    bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized_documents]
     # Train an LDA model on the bag-of-words corpus
    lda_model = gensim.models.ldamodel.LdaModel(
    corpus=bow_corpus,
    id2word=dictionary,
    num_topics=2,
    passes=10,
    alpha="auto",
    per_word_topics=True,
    )


    # # Extract the topics from the documents
    for i, document in enumerate(content):
        # Get the bag-of-words representation of the document
        bow_doc = dictionary.doc2bow(tokenized_documents[i])
        # Get the topic distribution for the document
        topic_dist, _, _ = lda_model.get_document_topics(bow_doc, per_word_topics=True)
        # Extract the top topic for the document
        top_topic = sorted(topic_dist, key=lambda x: x[1], reverse=True)[0][0]
        # Print the document and its top topic
        print(f"{document} => Topic {top_topic}")
    # ### the end of the tag function


   

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
                # thread_ts=message['ts']
                ts=ts
                # main_thread_ts = message['thread_ts']
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

conn.commit()
conn.close()